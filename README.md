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
- During each run, the script moves any bookmarks from the managed folder that
  are not present in the `managed_bookmarks.plist` to a folder named `Recovered
  Bookmarks-<Timestamp>`.
	- It also adds a link to a local html page with more details for users to
	  read.
	  - The help page is dynamically configured with data from the `managed_bookmarks.plist`.
- It then populates the managed bookmark folder with only the bookmarks
  configured.

## Configuration

You will probably want to customize the managed bookmarks and the "Why are my
Bookmarks Here?" page.

To do so, edit the `managed_bookmarks.plist` file to set the names of the
various properties and add in your desired bookmarks.
Top level keys include:
- `FolderName`: The name of the managed bookmarks folder
- `OrganizationName`: The name of your organization, used on the help page.
- `SupportWebsite`: The URL to your organization's support system, used on the
  help page.
- `SupportEmail`: The email address for your organization's email system, used
  on the help page.
- `Bookmarks`: An array of dicts reperenting the managed bookmarks. These will
  be added in the order they are specified.
	- Each bookmark should be a dict, with keys `title` and `URL`, like so:
	```
	<dict>
	  <key>title</key>
	  <string>Github for this project</string>
	  <key>URL</key>
	  <string>https://github.com/sheagcraig/ensure-safari-bookmarks</string>
	</dict>
	```

The help page includes an image that is left pleasingly blank by default.
However, if you would like to substitute your organization's logo or a photo,
overwrite the file `images/avatar.jpg` with desired image. If you want to
disable the ellipse mask, remove the class from the avatar image "header" near
the top of the `explanation.html` page.

There are some other sweet background images included in the images folder if
you want to toy around with a different palette.

You may also edit `explanation.html` to suit your organization's needs. The
marked script will sub in the text specified in the managed_bookmarks.plist.
For exmaple, any use of the managed bookmarks folder name found in `span` tags
with class of `managed_folder` will be swapped with the name of your managed
folder. This way, you can change your mind at a later date without having to
update the html; nor do you _need_ to modify the html that comes with it.

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

## When Will There be Support for Other Browsers
Send me information on how they manage their bookmarks and I'll add it!

## Great Stuff!
Thanks to Greg Neagle for sharing FoundationPlist.
Thanks to @n33co and html5up.net for the sweet HTML template (CCA FTW!)

## The Name
You may ask, why is this called Marked?

Because BM-Manager just wouldn't do.
