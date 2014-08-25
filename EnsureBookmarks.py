#!/usr/bin/python
"""EnsureBookmarks.py

Script that ensures a folder of bookmarks is included in the Safari bookmarks
bar.
Copyright (C) 2014 Shea G Craig <shea.craig@da.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


import os
import shutil

import FoundationPlist
import SafariBookmarks


MANAGED_BOOKMARKS = '/Library/Management/Bookmarks/managed_bookmarks.plist'
BOOKMARKS_FILE = os.path.expanduser('~/Library/Safari/Bookmarks.plist')


def main():
    # Parse our management settings.
    managed_bookmarks_plist = FoundationPlist.readPlist(MANAGED_BOOKMARKS)
    managed_bookmark_folder = managed_bookmarks_plist['FolderName']
    managed_bookmarks = managed_bookmarks_plist['Bookmarks']

    # If a Bookmarks.plist file doesn't exist, SafariBookmarks will create one.
    bookmarks = SafariBookmarks.SafariBookmarks(BOOKMARKS_FILE)

    # Ensure our folder is in the Bookmarks Bar.
    if not bookmarks.find(managed_bookmark_folder, bookmarks.bookmarks_bar):
        folder = SafariBookmarks.BookmarkFolder(managed_bookmark_folder)
        bookmarks.add_folder(bookmarks.bookmarks_bar, folder, 0)

    # Clear the original contents
    managed_folder = bookmarks.find(managed_bookmark_folder,
                                    bookmarks.bookmarks_bar)
    managed_folder['Children'] = []

    for bookmark in managed_bookmarks:
        bm = SafariBookmarks.Bookmark(bookmark['title'], bookmark['URL'])
        managed_folder['Children'].append(bm)

    bookmarks.save()


if __name__ == '__main__':
    main()
