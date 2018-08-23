# Categorize-images

The aim of this project is to provide a light-weight multi-platform script to quikly classify a collection of images stored on a directory, using your default browser to preview images. This is useful both for building training data that will then be used as an imput to train a classifier, or by itself as a way of making a catalog of a collection of images.

## Requirements ##
This script works with Python 3.0 or higher. Probably all of the packages it uses are part of your Python 3 library by default. This are the packages:
* pillow
* os
* sys
* re
* webbrowser
* argparse

## Usage ##
Fork this repository and run the cateforize-images.py from a terminal window. This script takes two required possitional arguments:
* A directory in your local filesystem that contains the images you want to classify.
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
*f: Classify all remaining images in a subdirectry as the base class. This is useful when each subdirectory represents a document and your are looking for specific pages within the document that are always next to each other, and therefore once you went through the last one you don't need to go through the rest (because you can safely assume they are part of the base category).
*b: Goes back and delates the lastly classified image, so you can reclassify it. You can go further back by repeatedly entering b. This speeds up the classification in cases where most images belong to the base category, as you can classify them quickly and go back when you see that another class passed by.

### Auxiliary code to extract images ###
The repository also includes a script called extract-images.py. This is a script that is very specific to a particular application I worked on, but may be helpful for others if facing a similar situation (even directly or providing a good baseline to adapt the code). The script will loop through a directory structure and create a mirror directory structure with symbolic links to images and jpg images for jpg images embedded into Pdf's. The part that extracts jpg images embbeded into Pdf's was build on top of a code I found in [Ned Batchelder's blog](https://nedbatchelder.com/blog/200712/extracting_jpgs_from_pdfs.html).

Comments on how to improve these scripts are Welcome!

