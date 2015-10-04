# Marked

I needed to ensure that our users always had a folder of important hyperlinks
on their managed laptops. Even if they deleted the folder, or puffed it up with
their own misguided TODO list and youtube video links, I wanted it to always
have exactly what we specified; no more, no less, but without fooling around
with the user's bookmarks.

So I made this. Here's how it works:
- A LaunchAgent runs a python script every time the user logs in.
- The python script looks at a data file, `managed_bookmarks.plist` for its
  configuration.
- The script ensures that Safari has a Bookmarks.plist file, and then ensures
  that the `FolderName` folder exists.
- During each run, the script clears the contents of the managed bookmark
  folder, and replaces it with the specified bookmarks.
- If the user has put any new bookmarks into the managed folder, they get moved
  into a folder named `Recovered Bookmarks`.

## Configuration

Edit the `managed_bookmarks.plist` file to set the name of the managed
folder with the value of the `FolderName` key.  Then, edit the array of
Bookmarks to include your desired bookmarks, in order. Each bookmark should be
a dict, with keys `title` and `URL`, like so:
```
<dict>
  <key>title</key>
  <string>Github for this project</string>
  <key>URL</key>
  <string>https://github.com/sheagcraig/ensure-safari-bookmarks</string>
</dict>
```

I have included a Makefile for building a package with The Luggage. Otherwise,
deployment is left up to the admin.

If you wish, you can rename the LaunchAgent to match your organization, as well
as move the supporting python files and data files wherever you please. The
Makefile documents where I put them if you want an example.

## Notes This system should handle all of the different states Bookmarks.plist
can be in. Specifically, when a new user account first uses Safari, the file
doesn't even exist. The SafariBookmarks class will create one. (I don't bother
to replicate the default bookmarks into this new Bookmarks.plist) If the
managed folder does not exist, it will create one. If the managed folder _does_
exist, but differs, it will get fixed.

This definitely falls into the "get-it-done" style of projects. (See the find()
method...) When I get more time, I plan to go through and streamline the
supporting classes and make greater use of PyObjC to better handle some of the
annoying issues.

For example, most of the elements of the bookmarks file have an array named
"Children" that stores the subelements. However, if the array is empty, the
"Children" array and key are pruned, probably when they get compacted into
binary by the preferences system. Currently this is fixed just by testing for
its existence and adding it back in if needed, but I imagine making greater use
of NSData types and methods would handle this.

If you wanted to be really draconian, I imagine you could change the
LaunchAgent to execute whenever the Bookmarks.plist file changed. For me, once
every login is sufficient.

## The Name
You may ask, why is this called Marked?

Because BM-Manager just wouldn't do.
