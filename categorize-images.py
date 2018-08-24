#! python
'''
This script will loop through the directory you selected as the first argument, and show you each image located in that directory tree using your default browser. By default, the image will be displayed with a height of 600 pixels, but you can modify this value by giving the desire number of pixels as an integer to the -hg flag.

You will be asked to classify each image, and the results will be saved to the csv file you selected as the second argument. If the file already exists, the script will pick up the work from where you left it last time and append the new results to the file. If it does not exist, it will create the file. You can use the -o flag to overwrite an existing file.

You can add categories editing the categories.csv file before running this script (following the same structure that the base class, that is, a unique integer and a description separated by a comma), or on the fly by entering "create" when asked to classify an image. If you modify the file, enter a new line (press enter) at the end of your last category to be able to add categories on the fly later on.

The script requires a directory tree that at the end leads to images. Everything that is not recognized by pillow as an image will be ignored. You can use the extract-images.py auxiliary code to build this tree structure if you have PDF's that encapsulate jpg images. See the heading of that code for more information.
'''

import os,sys
import argparse
from PIL import Image
import re
import webbrowser
from time import sleep

def main():
    '''
    This function parse the arguments and explain the user how to use de code and makes sure the user know what is doing if using the overwrite flag. Then, it calls the interate_trhough_tree function that does most of the work with.
    '''
    # Parsing the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("search_dir", help="directory you will classify")
    parser.add_argument("save_file", help="csv file where the classification will be saved")
    parser.add_argument("-o", "--overwrite", help="overwrite save_file if exists",
                        action="store_true")
    parser.add_argument("-hg", "--height", help="Height of image in browsers in pixels (enter an integer). Default is 600px",
                        type=int,default=600)
    args = parser.parse_args()
    overwrite  = args.overwrite
    height  = args.height

    global inputpath, outputfile
    inputpath  = args.search_dir
    outputfile = args.save_file

    # If the path to the target dir is absolute, we make it relative to
    # the directory where this script is run from
    if os.path.isabs(inputpath):
        inputpath  = os.path.relpath(inputpath,os.getcwd())

    # We exit the program if the directory to the outputfile does not exist
    if not os.path.isdir(os.path.split(outputfile)[0]):
        sys.exit('The path to {0} does not exist.'.format(outputfile))

    # We exit the program if the directory is not found
    if not os.path.isdir(inputpath):
        sys.exit('{0} is not a valid directory.'.format(inputpath))

    # Welcome message:
    print("\nWelcome to the check-files script.\n\nThis script will loop through the directory you selected as the first argument, and show you each image located in that directory tree using your default browser. By default, the image will be displayed with a height of 600 pixels, but you can modify this value by giving the desire number of pixels as an integer to the -hg flag.\n\nYou will be asked to classify each image, and the results will be saved to the csv file you selected as the second argument. If the file already exists, the script will pick up the work from where you left it last time and append the new results to the file. If it does not exist, it will create the file. You can use the -o flag to overwrite an existing file.\n\nYou can add categories editing the categories.csv file before running this script (following the same structure that the base class, that is, a unique integer and a description separated by a comma), or on the fly by entering create when asked to classify an image. If you modify the file, enter a new line (press enter) at the end of your last category to be able to add categories on the fly later on.\n\nThe script expects a directory tree filled with images. Everything that is not recognized by pillow as an image will be ignored. You can use the extract-images.py auxiliary code to build this tree structure if you have PDF's that encapsulate jpg images. See the heading of that code for more information.")

    display_categories()

    # Editing template.html to write pixel height
    with open('template.html','r')as temp:
        temp_lines = temp.readlines()
        temp_lines[14]='  height:{0}px;\n'.format(height)
        temp.close()

    with open('template.html','w') as temp:
        temp.writelines(temp_lines)
        temp.close()

    # We open the html_template in the user's default browser:
    print('\nThe script will now open your default web browser, where images will be displayed. ')
    webbrowser.open('file://{0}'.format(os.path.abspath('template.html')))

    # If the overwrite flag is on, we confirm the user know what is doing.
    if overwrite:
        o = input("\nYou selected the overwrite flag. Are you sure you want to overwrite {0}? All saved classifications will be lost [y/n]: ".format(outputfile))
        if   o in ['n','N','No','NO']:
            sys.exit('Try again without the overwrite flag')
        elif o in ['y','Y','yes','Yes','YES']:
            interate_through_tree(inputpath,outputfile,overwrite)
        else:
            sys.exit('Not a valid input')

    # If no overwrite flag exists and file exists, we inform of what will happendself.
    # That is, that new data will be appended to the existing file.
    elif os.path.exists(outputfile):
        print('\n{0} already exists. Files that have been already classified will be skipped, and the classification will be appended to {0}'.format(outputfile))
        interate_through_tree(inputpath,outputfile,overwrite)

    # Otherwise we just interate through the file tree
    else:
        interate_through_tree(inputpath,outputfile,overwrite)

def interate_through_tree(inputpath,outputfile,overwrite):
    '''
    This function is the core of the program. It iterates trhough the non-visited images of the directory tree for classification.
    '''
    # If the file does not exists or the overwrite flag is on, we create/overwrite the file.
    if (not os.path.isfile(outputfile)) or overwrite:
        with open(outputfile,'w') as of:
            of.write('path,class\n')

    # We reed the file to capture what files have been visited
    with open(outputfile,'r') as of:
        past_paths = [re.search("^(.*),",line).group(1)  for line in of]

    for dirpath, dirnames, filenames in os.walk(inputpath):

        # We are not interested in directories with no files
        if len(filenames)==0:
            continue

        # This will break the loop through the files in one subdirectory. Used for
        # "express classification" when you know all the files that are left are
        # from the base class.
        for i, file in enumerate(sorted(filenames)):

            # The absolute path to the file
            file_path = os.path.join(dirpath,file)

            # Skip file if already classified
            if file_path in past_paths:
                continue

            # Skip if file is not an image that pil can open
            try:
                img = Image.open(file_path)
            except:
                print('\nThe file {0} was not recognized by pillow as an image. Continuing to next file'.format(file_path))
                continue

            # This loop allow the user to make mistakes and come back to the same file to do it right

            while True:
                print('\nOpening {0} in your browser for classification'.format(file_path))
                # We load the image and save it in the tmp folder
                img = Image.open(file_path)
                img_temp = 'current_image.jpg'
                img.save(img_temp)

                # We prompt the user to enter a choice.
                choice = input("\n\tPlease enter class (enter h to see options): ")

                with open('categories.csv','r') as categories:
                    global cat_dict
                    cat_dict  = {key:des for (key,des) in iter([tuple(cat.split(',')) for cat in categories])}
                    valid_cat = cat_dict.keys()
                    categories.close()

                # If the choice is valid (1,2,3), we save it to the file.
                if choice in valid_cat:
                    with open(outputfile,'a') as of:
                        of.write('{0},{1}\n'.format(file_path,choice))
                        of.close()
                    print('\n\tImage classified as "{0}" ({1})'.format(cat_dict[choice].strip(),choice))
                    break

                elif bool(re.search('^f([0-9]*)?( [0-9]*)?',choice)):
                    # Classify n lines as category provided by second argument.
                    n,c = re.search('^f([0-9]*)?( [0-9]*)?',choice).groups()

                    # If n not provided, then default is all remaining images in subdirectory.
                    if n in ['',None]:
                        n = len(sorted(filenames)[i:])
                    else:
                        n = int(n.strip())

                    # If c (category to use in forward classification) is not provided, default is using base category.
                    if c in ['',None]:
                        c = '1'
                    elif c.strip() in valid_cat:
                        c = c.strip()
                    else:
                        print(c)
                        print('\t Not a valid category. Try again (enter h to see valid categories)')
                        continue
                    fast_forward(filenames,dirpath,i,n,c)
                    # If the subdirectory is the last one, fast forward will run at the end the interate_through_tree function and skip all files (because all of them have been classified). The the program will exit the function and prompt you to classify the image that was open before entering f. For that reason, we need to exit the program if we reach this point
                    sys.exit(0)

                elif bool(re.search('^b([0-9]*)?',choice)):
                    # Removing last n lines of the saved file and running this function again with the overwrite option off to classify the past image again
                    try:
                        n = int(re.search('^b( ?[0-9]*)',choice).group(1).strip())
                    except:
                        n= 1
                    move_backward(n)

                elif choice=='h':
                    display_categories()
                    continue

                elif choice=='q':
                    os.remove(img_temp)
                    sys.exit('\n\t Exiting. Your work has been saved and you can retake it from where you left it.')

                elif choice=='create':
                    cat=input("\n\t\tPlease enter a unique integer for your new category: ")
                    try:
                        int(cat)
                    except:
                        print('\n\t\tProvided category is not an integer, try again entering an integer.')
                        continue
                    if cat in valid_cat:
                        print("\n\t\tThis integer is already used for another category, try again selecting a unique integer to create a new category")
                        continue
                    else:
                        des=input("\n\t\tPlease enter a brief description for your new category: ")
                        with open('categories.csv','a') as categories:
                            categories.write('{0},{1}\n'.format(cat,des))
                            categories.close()
                        with open(outputfile,'a') as of:
                            of.write('{0},{1}'.format(file_path,cat))
                            of.close()
                            print('\n\t\tImage classified as "{0}" ({1})'.format(des,cat))
                        break

                else:
                    print('\n\tNot a valid input. Type h to see available options.')
                    continue
    try:
        os.remove(img_temp)
    except:
        pass

def display_categories():
        print('\nYou have the following available Categories:')
        with open('categories.csv','r') as classes:
            for type in classes:
                try:
                    print('\t- Enter {0} to classify image as "{1}"'.format(*[x.strip() for x in type.split(',')]))
                except:
                    sys.exit('Check syntax of categories.csv file. Each class represents a row with a unique integer and a short description, separated by a comma.')
        print('\nAnd the following default options:')
        print('\t- Enter fx y to classify the following x images in the subdirectory as part of the y category. If x is ommited, default is all remaining unclassified images in subdirectory. If y is ommited, default is to use the base category.')
        print('\t- Enter h to see this message.')
        print('\t- Enter create to create a new category on the fly.')
        print('\t- Enter bx to remove the classification of the last x images and classify them again (if x is ommited, default is to delate classification of the last classified image).')
        print('\t- Enter q to exit the script (your result from the images you have classified have been saved).')
        print('You may also add new categories by editing the categories.csv file before running this script.')

def fast_forward(filenames,dirpath,i,n,c):
    '''
    This function will authomatically classify the n following Images as part of the base category, showing each image in the browser for 200 microseconds.
    '''
    move_forward=i+min(n,len(sorted(filenames)[i:]))
    with open(outputfile,'a') as of:
        for file in sorted(filenames)[i:move_forward]:
            file_path = os.path.join(dirpath,file)

            # Show Images in browser passing fast
            img = Image.open(file_path)
            img_temp = 'current_image.jpg'
            img.save(img_temp)

            #Saving file as base category and informing the users
            of.write(file_path+',1\n')
            print(cat_dict,c)
            print('\n\t\t{0} classified as "{1}" ({2})\n'.format(file_path,cat_dict[c].strip(),c))
            sleep(0.2)
    of.close()
    interate_through_tree(inputpath,outputfile,False)

def move_backward(n):
    '''
    This function will delate the classification of the past n images and open your browser in the first of the delated images to restart the classification.
    '''
    with open(outputfile,'r')as temp:
        temp_lines = temp.readlines()
        temp.close()

    with open(outputfile,'w') as temp:
        temp.writelines(temp_lines[:-n])
        temp.close()
    interate_through_tree(inputpath,outputfile,False)

if __name__=='__main__':
    main()
