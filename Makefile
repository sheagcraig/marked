include /usr/local/share/luggage/luggage.make

TITLE=marked
REVERSE_DOMAIN=com.github.sheagcraig
PAYLOAD=\
		pack-Library-LaunchAgents-com.github.sheagcraig.marked.plist\
		pack-Library-Application-Support-Marked\

PACKAGE_VERSION=1.0

marked: l_Library_Application_Support
	@sudo mkdir ${WORK_D}/Library/Application\ Support/marked
	@sudo chown 0:80 ${WORK_D}/Library/Application\ Support/marked
	@sudo chmod 755 ${WORK_D}/Library/Application\ Support/marked

pack-Library-Application-Support-Marked: marked
	@sudo ${CP} marked.py ${WORK_D}/Library/Application\ Support/marked
	@sudo ${CP} FoundationPlist.py ${WORK_D}/Library/Application\ Support/marked
	@sudo ${CP} SafariBookmarks.py ${WORK_D}/Library/Application\ Support/marked
	@sudo ${CP} managed_bookmarks.plist ${WORK_D}/Library/Application\ Support/marked
	@sudo chown -R 0:80 ${WORK_D}/Library/Application\ Support/marked
	@sudo chmod -R 755 ${WORK_D}/Library/Application\ Support/marked