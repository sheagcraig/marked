#!/usr/bin/python
"""SafariBookmarks.py

Represents Safari Bookmarks
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
import subprocess

import FoundationPlist


class SafariBookmarks(object):
    """Encapsulate a Bookmarks.plist file in a more useful way."""
    def __init__(self, filename=os.path.expanduser(
            "~/Library/Safari/Bookmarks.plist")):
        self.filename = filename
        try:
            self._bm = FoundationPlist.readPlist(self.filename)
        except:
            self.create()
            self.__init__(filename)

        self.bookmarks_bar = self.find("BookmarksBar")
        self.bookmarks_menu = self.find("BookmarksMenu")
        self.history = self.find("History")
        self.reading_list = self.find("com.apple.ReadingList")

    def create(self):
        """Build a Bookmarks.plist from scratch."""
        for key, value in {'Children': '()', 'Title': '',
                           'WebBookmarkType': 'WebBookmarkTypeList'}.items():
            subprocess.check_call(['defaults', 'write',
                                   os.path.abspath(self.filename), key, value])

        self._bm = FoundationPlist.readPlist(self.filename)
        bookmarks_menu = BookmarkFolder("BookmarksMenu")
        bookmarks_bar = BookmarkFolder("BookmarksBar")
        self.add_folder(self._bm, bookmarks_menu)
        self.add_folder(self._bm, bookmarks_bar)
        self.save()

    def find(self, title, node=None):
        """Find an element by its Title."""
        # Super heinous. Need to refactor.
        # Needs to finish with a single return. As you work down, you
        # eliminate the non-desired states.

        # Start at the root if no node given
        if not node:
            node = self._bm

        node_type = node.get("WebBookmarkType")

        # Nodes can be of three types: list, leaf, or proxy
        # For some annoying reason the title property is different depending on
        # the type.
        # The only "proxy" I've seen is "History"
        if node_type == "WebBookmarkTypeList":
            node_title = node.get("Title")
            print(node_type, node_title)
            if node_title == title:
                return node
            if node.get("Children"):
                for next_node in node.get("Children"):
                    result = self.find(title, next_node)
                    if result:
                        return result
        elif node_type == "WebBookmarkTypeLeaf":
            node_title = node.get("URIDictionary").get("title")
            print(node_type, node_title)
            if node_title == title:
                return node
        elif node_type == "WebBookmarkTypeProxy":
            node_title = node.get("Title")
            print(node_type, node_title)
            if node_title == title:
                return node

    def add_folder(self, node, folder, index=None):
        # Must be a List
        if not node.get("WebBookmarkType") == "WebBookmarkTypeList":
            raise ValueError("Node must be of type 'WebBookmarkTypeList'")
        self._ensure_children(node)
        if index:
            node['Children'].insert(index, folder)
        else:
            node['Children'].append(folder)

    def add_bookmark(self, node, bookmark, index=None):
        # Must be a List
        if not node.get("WebBookmarkType") == "WebBookmarkTypeList":
            raise ValueError("Node must be of type 'WebBookmarkTypeList'")
        self._ensure_children(node)
        if index:
            node['Children'].insert(index, bookmark)
        else:
            node['Children'].append(bookmark)

    def _ensure_children(self, node):
        """Make sure a Children array is available."""
        # It seems that the system will remove empty Children arrays under some
        # circumstances. So we have to put one back in prior to
        # adding-operations.
        #
        # We use try/except since NSDict doesn't have a get method.
        try:
            node['Children']
        except KeyError:
            node['Children'] = []

    def save(self, filename=None):
        if not filename:
            FoundationPlist.writePlist(self._bm, self.filename)
        else:
            FoundationPlist.writePlist(self._bm, filename)


class BookmarkFolder(dict):
    def __init__(self, name):
        super(BookmarkFolder, self).__init__()
        self['Title'] = name
        self['Children'] = []
        self['WebBookmarkType'] = 'WebBookmarkTypeList'

    def add_bookmark(self, bookmark, index=None):
        # Must be a List
        if index:
            self['Children'].insert(index, bookmark)
        else:
            self['Children'].append(bookmark)


class Bookmark(dict):
    def __init__(self, title, url):
        """Construct a bookmark for use in a Safari bookmark file."""
        super(Bookmark, self).__init__()
        self['URIDictionary'] = {'title': title}
        self['URLString'] = url
        self['WebBookmarkType'] = 'WebBookmarkTypeLeaf'