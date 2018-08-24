# Categorize-images

The aim of this project is to provide a light-weight multi-platform script to quickly classify a collection of images stored on a directory, using your default browser to preview images. This is useful both for building training data that will then be used as an input to train a classifier, or by itself as a way of making a catalog of a collection of images.

## Requirements ##
This script works with Python 3.0 or higher. Probably all of the packages it uses are part of your Python 3 library by default. This are the packages:
* pillow
* os
* sys
* re
* webbrowser
* argparse
* time

## Usage ##
Fork this repository and run the categorize-images.py from a terminal window. This script takes two required positional arguments:
* A directory in your local file system that contains the images you want to classify.
* A csv file where the classifications will be saved. Each image you classify corresponds to a line in this file, that indicates the absolute path to the image and its class, separated by a comma.

The following optional flags are available:
* -o --overwrite: Overwrites an existing csv file. If not specified, the script will create a file if a file with the provided name does not exist, or append the classification to an existing file if it exists. In the later case, the script will skip all files that have already been classified.
* -hg -- height: Specify the height in pixels with which images are displayed in your browser.

The script will skip any file in the directory that is not readable by pillow, so be aware of this fact if you have uncommon image formats.

To include your own categories, you have to edit the categories.csv file. Append your new categories to this file following the same structure than the base category that is included there, that is, an integer and a brief description separated by a comma. Be sure to press enter (add a new line) when entering your last category. Your can also add categories on the fly when running the script by entering "create" when asked for the category of an image.

### Default allowed inputs ###
By default, the script accepts the following inputs when asking for a class:
*1: Base category, it is written into categories.csv.
*h: Display the allowed inputs, which are given by the default allowed inputs plus the classes written into the categories.csv file.
*create: Creates new category on the file and appends it to the categories.csv file.
*f x: Classify the following x images in the current subdirectory as the base class, or all non-classified images in the current subdirectory if x is larger than the number of non classified images in the current subdirectory. If an integer is not specified, all the images that have not been classified in the current subdirectory will be classified as the base class. These images will be display on your browser at a rate of 5 images per second, so you can inspect whether all images where in fact part of the base class.
*b x: Delate the classification of the last x classified images from the output database, and goes back to reclassify those images. If no integer is specified, delates only the last classified image.

### Auxiliary code to extract images ###
The repository also includes a script called extract-images.py. This is a script that is very specific to a particular application I worked on, but may be helpful for others if facing a similar situation (even directly or providing a good baseline to adapt the code). The script will loop through a directory structure and create a mirror directory structure with symbolic links to images and jpg images for jpg images embedded into Pdf's. The part that extracts jpg images embbeded into Pdf's was build on top of a code I found in [Ned Batchelder's blog](https://nedbatchelder.com/blog/200712/extracting_jpgs_from_pdfs.html).

Comments on how to improve these scripts are Welcome!
