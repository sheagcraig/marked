#!/usr/bin/python
# Copyright (C) 2014, 2015 Shea G Craig
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""marked.py

Script that ensures a folder of bookmarks is included in the Safari
bookmarks bar.
"""


import datetime
import os
import re
import shutil

import FoundationPlist
import SafariBookmarks

# Edit ORGANIZATION to specify your organization's name automatically
# in the explanation.html.
MARKED_FOLDER = "/Library/Application Support/marked"
MANAGED_BOOKMARKS = os.path.join(MARKED_FOLDER, "managed_bookmarks.plist")
EXPLANATION = os.path.join(MARKED_FOLDER, "explanation.html")
USER_FOLDER = os.path.expanduser("~/Library/Application Support/marked")
USER_EXPLANATION = os.path.join(USER_FOLDER, "explanation.html")
BOOKMARKS_FILE = os.path.expanduser("~/Library/Safari/Bookmarks.plist")


def move_unwanted_bookmarks(bookmarks, managed_folder,
                            managed_bookmarks_plist):
    """Move difference of managed bms and current bms into backup."""
    # For each bookmark in the managed folder, if it's one we want,
    # remove it, as it will get added in again later. If any are left
    # afterwards, rename the folder, and add a link to the explanation
    # html locally.

    # We have to remove _after_ collecting the good ones because
    # NSCFArray can't be mutated while enumerating.
    managed_bookmarks = managed_bookmarks_plist["Bookmarks"]
    removals = []
    for bookmark in managed_folder["Children"]:
        for managed_bookmark in managed_bookmarks:
            if (bookmark.get("URIDictionary").get("title") ==
                managed_bookmark["title"]) and (
                    bookmark.get("URLString") == managed_bookmark["URL"]):
                removals.append(bookmark)
    # If any are left, rename the folder to "move" it.
    for bookmark in removals:
        managed_folder["Children"].remove(bookmark)
    if managed_folder["Children"]:
        with open(EXPLANATION, "r") as explanation:
            explanation_text = explanation.read()
        explanation_text = sub_text(explanation_text, managed_bookmarks_plist)

        if not os.path.exists(USER_FOLDER):
            os.mkdir(USER_FOLDER)

        with open(USER_EXPLANATION, "w") as explanation:
            explanation.write(explanation_text)

        assets = os.path.join(USER_FOLDER, "assets")
        if os.path.exists(assets):
            shutil.rmtree(assets)
        shutil.copytree(os.path.join(MARKED_FOLDER, "assets"), assets)

        images = os.path.join(USER_FOLDER, "images")
        if os.path.exists(images):
            shutil.rmtree(images)
        shutil.copytree(os.path.join(MARKED_FOLDER, "images"), images)

        bm = SafariBookmarks.Bookmark("Why are my Bookmarks Here?", "file://%s"
                                      % USER_EXPLANATION)
        managed_folder["Children"].append(bm)

        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
        managed_folder["Title"] = "Recovered Bookmarks-%s" % timestamp


def sub_text(text, plist):
    text = re.sub(
        r'<span class="managed_folder">.*</span>',
        '<span class="managed_folder">%s</span>' % plist["FolderName"],
        text)
    text = re.sub(r'Organization_Name', plist["OrganizationName"], text)
    text = re.sub(r'SUPPORT_WEBSITE', plist["SupportWebsite"], text)
    text = re.sub(r'SUPPORT_EMAIL', plist["SupportEmail"], text)
    return text


def main():
    # Parse our management settings.
    managed_bookmarks_plist = FoundationPlist.readPlist(MANAGED_BOOKMARKS)
    managed_bookmark_folder = managed_bookmarks_plist["FolderName"]
    managed_bookmarks = managed_bookmarks_plist["Bookmarks"]

    # If a Bookmarks.plist file doesn't exist, SafariBookmarks will
    # create one.
    bookmarks = SafariBookmarks.SafariBookmarks(BOOKMARKS_FILE)

    # Try to find the managed folder.
    managed_folder = bookmarks.find(managed_bookmark_folder,
                                    bookmarks.bookmarks_bar)
    # If managed folder exists, and it has unmanaged bookmarks,
    # rename it.
    if managed_folder:
        move_unwanted_bookmarks(bookmarks, managed_folder,
                                managed_bookmarks_plist)

    # Try to find again (will be gone if moved).
    managed_folder = bookmarks.find(managed_bookmark_folder,
                                    bookmarks.bookmarks_bar)

    # So if it's missing, create a new, blank managed folder.
    if not managed_folder:
        folder = SafariBookmarks.BookmarkFolder(managed_bookmark_folder)
        bookmarks.add_folder(bookmarks.bookmarks_bar, folder, 0)
        managed_folder = bookmarks.find(managed_bookmark_folder,
                                        bookmarks.bookmarks_bar)

    # Add the bookmarks.
    for bookmark in managed_bookmarks:
        bm = SafariBookmarks.Bookmark(bookmark["title"], bookmark["URL"])
        managed_folder["Children"].append(bm)

    bookmarks.save()


if __name__ == "__main__":
    main()
