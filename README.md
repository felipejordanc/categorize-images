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

Additionally, the script needs to have the following supportive files in the same directory to work:
* categories.csv
* template.html

Both files are part of this repository.

## Usage ##
Fork this repository and run the categorize-images.py from a terminal window. This script takes two required positional arguments:
* A directory in your local file system that contains the images you want to classify.
* A csv file where the classifications will be saved. Each image you classify corresponds to a line in this file, that indicates the relative path to the image and its class, separated by a comma. The path is relative to the directory from where you are running this script from.

The following optional flags are available:
* -o --overwrite (boolean): Overwrites an existing csv file. If not specified, the script will create a file if a file with the provided name does not exist, or append the classification to an existing file if it exists. In the later case, the script will skip all files that have already been classified. Default is False.
* -hg -- height (integer): Specify the height in pixels with which images are displayed in your browser. Default is 600.
* -v -- velocity (integer): Specify the number of images displayed by second in your browser when using the f option (see below). Default is 4.
* -noh -- no_half (boolean): Do not half the velocity at which images are displayed using the f option when using a non-base category (see below). Default is False.

The script will skip any file in the directory that is not readable by pillow, so be aware of this fact if you have uncommon image formats.

To include your own categories, you have to edit the categories.csv file. Append your new categories to this file following the same structure than the base category that is included there, that is, a unique value (either an integer or a string with no spaces) and a brief description separated by a comma. Be sure to press enter (add a new line) when entering your last category. Your can also add categories on the fly when running the script by entering "create" when asked for the category of an image.

### Default allowed inputs ###
By default, the script accepts the following inputs when asking for a class:
* 1: Base category, it is written into categories.csv.
* h: Display the allowed inputs, which are given by the default allowed inputs plus the classes written into the categories.csv file.
* create: Creates new category on the file and appends it to the categories.csv file.
* fx y: Classify the following x images in the current subdirectory as the y category, or all non-classified images in the current subdirectory if x is larger than the number of non classified images in the current subdirectory. If x is not specified, all images that have not been classified in the current subdirectory will be classified as the y category. If y is not specified, images will be classified using the base category. Images will be displayed in your browser at a rate of four images per second by default in the case of the base category, and two images per second for other categories. This behavior can be modified using the velocity and no_half flags.
* bx: Delate the classification of the last x classified images from the output database, and goes back to reclassify those images. If x is no specified, delates only the lastly classified image.

### Auxiliary code to extract images ###
The repository also includes a script called extract-images.py. This is a script that is very specific to a particular application I worked on, but may be helpful for others if facing a similar situation (even directly or providing a good baseline to adapt the code). The script will loop through a directory structure and create a mirror directory structure with symbolic links to images and jpg images for jpg images embedded into Pdf's. The part that extracts jpg images embbeded into Pdf's was build on top of a code I found in [Ned Batchelder's blog](https://nedbatchelder.com/blog/200712/extracting_jpgs_from_pdfs.html).

## Authors ##
Felipe Jordan [(go to github page)](https://github.com/felipejordanc)

Comments on how to improve these scripts are Welcome!
