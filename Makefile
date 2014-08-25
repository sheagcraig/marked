include /usr/local/share/luggage/luggage.make

TITLE=EnsureBookmarks
REVERSE_DOMAIN=com.github.sheagcraig
PAYLOAD=\
		pack-Library-LaunchAgents-com.github.sheagcraig.ensure_bookmarks.plist\
		pack-Library-ManagementItems\

PACKAGE_VERSION=1.0

management: l_Library
	@sudo mkdir ${WORK_D}/Library/Management
	@sudo chown 0:80 ${WORK_D}/Library/Management
	@sudo chmod 755 ${WORK_D}/Library/Management

bookmarks: management
	@sudo mkdir ${WORK_D}/Library/Management/Bookmarks
	@sudo chown 0:80 ${WORK_D}/Library/Management/Bookmarks
	@sudo chmod 755 ${WORK_D}/Library/Management/Bookmarks

pack-Library-ManagementItems: bookmarks
	@sudo ${CP} EnsureBookmarks.py ${WORK_D}/Library/Management/Bookmarks
	@sudo ${CP} FoundationPlist.py ${WORK_D}/Library/Management/Bookmarks
	@sudo ${CP} SafariBookmarks.py ${WORK_D}/Library/Management/Bookmarks
	@sudo ${CP} managed_bookmarks.plist ${WORK_D}/Library/Management/Bookmarks
	@sudo chown -R 0:80 ${WORK_D}/Library/Management/Bookmarks
	@sudo chmod -R 755 ${WORK_D}/Library/Management/Bookmarks