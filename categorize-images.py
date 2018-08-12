import os,sys
import argparse
from PIL import Image
import re
import webbrowser

def main():

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
    inputpath  = args.search_dir
    outputfile = args.save_file

    # If the paths are relative, we append the working directory
    if not os.path.isabs(inputpath):
        inputpath  = os.path.join(os.getcwd(),inputpath)
    if not os.path.isabs(outputfile):
        outputfile = os.path.join(os.getcwd(),outputfile)

    # We exit the program if the directory is not found
    if not os.path.isdir(inputpath):
        sys.exit('{0} is not a valid directory.'.format(inputpath))

    # Welcome message:
    print('\nWelcome to the check-files script.\n\nThis script will loop through the directory you selected as the first argument, and show you each image located in that directory tree using your default browser. By default, the image will be displayed with a height of 600 pixels, but you can modify this value by giving the desire number of pixels as an integer to the -hg flag.\n\nYou will be asked to classify each image, and the results will be saved to the csv file you selected as the second argument. If the file already exists, the script will pick up the work from where you left it last time and append the new results to the file. If it does not exist, it will create the file. You can use the -o flag to overwrite an existing file.\n\nYou can add categories editting the categories.csv file before running this script (following the same structure that the base class, that is, a unique integer and a description separated by a comma), or on the fly by entering "create" when asked to classify an image. If you modify the file, enter a new line (press enter) at the end of your last category to be able to add categories on the fly later on.\n\n')

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
    print('\n\n The script will now open your default web browser, where images will be displayed. ')
    webbrowser.open('file://{0}'.format(os.path.abspath('template.html')))

    # If the overwrite flag is on, we confirm the user know what is doing.
    if overwrite:
        o = input("\n\nYou selected the overwrite flag. Are you sure you want to overwrite {0}? All saved classifications will be lost [y/n]: ".format(outputfile))
        if   o in ['n','N','No','NO']:
            sys.exit('Try again without the overwrite flag')
        elif o in ['y','Y','yes','Yes','YES']:
            interate_through_tree(inputpath,outputfile,overwrite)
        else:
            sys.exit('Not a valid input')

    # If no overwrite flag exists and file exists, we inform of what will happendself.
    # That is, that new data will be appended to the existing file.
    elif os.path.exists(outputfile):
        print('\n\n{0} already exists. Files that have been already classified will be skipped, and the classification will be appended to {0}'.format(outputfile))
        interate_through_tree(inputpath,outputfile,overwrite)

    # Otherwise we just interate through the file tree
    else:
        interate_through_tree(inputpath,outputfile,overwrite)


def interate_through_tree(inputpath,outputfile,overwrite):
    for dirpath, dirnames, filenames in os.walk(inputpath):

        # We are not interested in directories with no files
        if len(filenames)==0:
            continue

        # If the file exists or the overwrite flag is on, we create/overwrite the file.
        if (not os.path.isfile(outputfile)) or overwrite:
            with open(outputfile,'w') as of:
                of.write('path,class\n')
            past_paths=[]

        # Otherwise, we reed the file to capture what files have been visited
        else:
            with open(outputfile,'r') as of:
                past_paths = [re.search("^(.*),",line).group(1)  for line in of]

        # This will break the loop through the files in one subdirectory. Used for
        # "express classification" when you know all the files that are left are
        # from the base class.
        breaker=False

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
                continue

            # If the breaker is on, the classify all remaining images in the
            # subdirectory as the base class.
            if breaker:
                with open(outputfile,'a') as of:
                    for file in sorted(filenames)[i:]:
                        # Show Images in browser passing fast
                        img = Image.open(file_path)
                        img_temp = 'current_image.jpg'
                        img.save(img_temp)

                        #Saving file as base category and informing the users
                        file_path = os.path.join(dirpath,file)
                        of.write(file_path+',1\n')
                        print('\n\{0} classified as "{1}" ({2})\n'.format(file_path,'base',1))
                    of.close()
                break

            # This loop allow the user to make mistakes and come back to the
            # same file to do it right

            while True:
                print('\n\nOpening file {0} in your browser for classification\n'.format(file))
                # We load the image and save it in the tmp folder
                img = Image.open(file_path)
                img_temp = 'current_image.jpg'
                img.save(img_temp)

                # We prompt the user to enter a choice.
                choice = input("\n\tPlease enter class (enter h to see options): ")

                with open('categories.csv','r') as categories:
                    #valid_cat = [cat.split(',')[0] for cat in categories ]
                    cat_dict  = {key:des for (key,des) in iter([tuple(cat.split(',')) for cat in categories])}
                    valid_cat = cat_dict.keys()
                    categories.close()

                # If the choice is valid (1,2,3), we save it to the file.
                if choice in valid_cat:
                    with open(outputfile,'a') as of:
                        of.write('{0},{1}\n'.format(file_path,choice))
                        of.close()
                    print('\n\{0} classified as "{1}" ({2})\n'.format(file_path,cat_dict[choice],choice))
                    break

                elif choice=='f':
                    sure=input('\n\tAre you sure you have pass through all census pages [y/n]?')
                    if sure in ['y','Y','yes','YES']:
                        breaker=True
                        with open(outputfile,'a') as of:
                            of.write(file_path+',1\n')
                            of.close()
                            print('\n\{0} classified as "{1}" ({2})\n'.format(file_path,'base',1))
                        break
                    elif sure in ['n','N','no','NO']:
                        continue

                    else:
                        print("\n\t\tNot valid input, only accepts y or n")
                        continue

                elif choice=='h':
                    display_categories()
                    continue

                elif choice=='q':
                    os.remove(img_temp)
                    sys.exit('\n\t Exiting. Your work has been saved and you can retake it from where you left it.')

                elif choice=='create':
                    cat=input("\n\tPlease enter a unique integer for your new category: ")
                    if cat in valid_cat:
                        print("\n\t\tThis integer is already used for another category. You will be asked to classify this image again. Type create and select a unique integer to create a new category")
                        continue
                    else:
                        des=input("\n\tPlease enter a brief description for your new category: ")
                        with open('categories.csv','a') as categories:
                            categories.write('{0},{1}\n'.format(cat,des))
                            categories.close()
                        with open(outputfile,'a') as of:
                            of.write('file_path,{0}'.format(cat))
                            of.close()
                            print('\n\{0} classified as {1} ({2})\n'.format(file_path,des,cat))
                        break

                else:
                    print('Not a valid input.\n')
                    display_categories()
                    continue
    try:
        os.remove(img_temp)
    except:
        pass

def display_categories():
        print('From the classes you have in your categories.csv file, this are the instructions for classifying an image:\n\n')
        with open('categories.csv','r') as classes:
            for type in classes:
                try:
                    print('\t- Enter {0} to classify image as {1}'.format(*type.split(',')))
                except:
                    sys.exit('Check syntax of categories.csv file. Each class represents a row with a unique integer and a short description, separated by a comma.')
        print('\t- Enter f to classify the rest of the images in a directory as the base category (1)')
        print('\n\t- Enter h to see the available categories and their descriptions.')
        print('\n\t- Enter create to create a new category on the fly.')

if __name__=='__main__':
    main()