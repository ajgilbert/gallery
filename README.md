Usage:

  1. Clone this repository and make sure that the `gallery.py` script is in your `$PATH`
  2. Run script on a directory containing some images: `gallery.py path/to/some/dir` 
  3. An `index.html` file will be created in that directory and all subdirectories recursively

Notes:
 
 - Images must be png format and have the extension `.png`
 - Files with the same name but different extensions will be linked automatically in the gallery
 - A search box is added at the top which accepts regular expressions for filtering images in the gallery
 - It is possible to define attributes that can be assigned to each image. These should be specified in a `.json` file with the same name as the image, with the format:
 
 ```json
 {
    "ATTRIBUTE1" : "VALUE1",
    "ATTRIBUTE2" : "VALUE2"
 }
 ```
These json files will be read automatically. A set of buttons will be created for each attribute with one button per value that can be used to quickly select the subset of images that were assigned that value.
 - Other non-image files will be linked at the bottom of the page
 - A download link is provided on each page which will generate a zip file of the directory contents
