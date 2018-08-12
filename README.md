# categorize-images

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
Clone this repository and run the cateforize-images.py from a terminal window. This script takes two required possitional arguments:
* A directory in your local filesystem that contains the images you want to classify.
* A csv file where you will store your classification.

The following optional flags are available:
* -o --overwrite: Overwrites an existing csv file. If not specified, the script will create a file if a file with the provided name does not exist, or append the classification to an existing file if it exists. In the later case, the script will skip all files that have already been classified.
* -hg -- height: Specify the height in pixels with which images are displayed in your browser.

Follow the instructions in the script to learn how to include categories.
