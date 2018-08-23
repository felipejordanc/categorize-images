#! python
'''
This script is will replicate the tree structure of the directory privided
in the original_dir argument, and make a mirror of that directory in a
new directory whose location is given by the target_dir argument.

Images within PDF's in the original directory will be stored as different jpg images
in the target directy, while images in the original directory will have a symbolic link
in the target directory.

The scripts serves as a prepocess stage before classifying images using the categorize-images.py script.
Usage:

extract_img1.py original_dir target_dir [-o]

author: Felipe Jordan*
* The part of the code that extracts the jpg from the pdf is a modification of Ned Batchelder's code available at
  https://nedbatchelder.com/blog/200712/extracting_jpgs_from_pdfs.html
'''


from __future__ import print_function
import sys, time
import os
import argparse
import shutil
import re

def main():

    print("This script is will replicate the tree structure of the directory privided in the original_dir argument,and make a mirror of that directory in a new directory whose location is given by the target_dir argument.\n\nImages within PDF's in the original directory will be stored as different jpg imagesin the target directy, while images in the original directory will have a symbolic link in the target directory.\n\nThe scripts serves as a prepocess stage before classifying images using the categorize-images.py script.\n\nThe script will currently recognize as images the formats with extensions that match the patterns given in the regular expression of line 103. If you are dilling with another format, just add the desired extension.")

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("original_dir", help="Directory where original files are")
    parser.add_argument("target_dir", help="Directory where you will save images")
    args = parser.parse_args()
    original_dir = args.original_dir
    target_dir   = args.target_dir

    # For both directories, create absolute dir if a relative dir is provided.
    if not os.path.isabs(original_dir):
        original_dir_abs  = os.path.abspath(original_dir)
    else:
        original_dir_abs = original_dir

    if not os.path.isabs(target_dir):
        target_dir_abs  = os.path.abspath(target_dir)
    else:
        target_dir_abs = target_dir

    # Some exceptions
    if original_dir_abs==target_dir_abs:
        sys.exit('Directories can not be the same')
    if not os.path.exists(original_dir_abs):
        sys.exit('Directory does not exist')

    #Create tardet directory. If it already exists, it will ask the user
    # if he wants to overwrite it
    if os.path.exists(target_dir_abs):
        choice = input("The target directory already exists. Do you want to overwrite it? (y/n):")
        if bool(re.search(r'y(es)?',choice,re.IGNORECASE)):
            shutil.rmtree(target_dir_abs)
        else:
            sys.exit()
    os.mkdir(target_dir_abs)

    # Create CSV that will save a report of what happened to each
    # original file.
    outputfile = os.path.join(target_dir_abs,'report.csv')
    output_file = open(outputfile,'w')
    output_file.write('dir,file,extension,action\n')

    # Loop through the dir structure
    for dirpath, dirnames, filenames in os.walk(original_dir_abs):

        # Skipping empty directories
        if len(os.listdir(dirpath))==0:
            continue

        # Getting the directory in the new target dir structure that mimics
        # the one we are loopin now. Note this is not necessary if there are
        # no subdirectories.
        continuation_path   = os.path.relpath(dirpath,start=original_dir_abs)
        target_dirpath      = os.path.abspath(os.path.join(target_dir_abs,continuation_path))
        print(target_dir_abs,target_dirpath)
        if not target_dir_abs==target_dirpath:
            os.mkdir(target_dirpath)

        # Now we loop through the files and decide what to do:
        print('\nLooping through directory {0}'.format(dirpath))

        for i , file_name in enumerate(sorted(filenames)):
            extension     = re.search(r'\.(.*)$',file_name)[1]
            file_path     = os.path.join(dirpath,file_name)

            if bool(re.search(r'\.pdf$',file_name)):
                print("\tConverting PDF " + file_name + " to jpg:")
                convert_to_images(file_path,target_dirpath)
                output_file.write('{0},{1},{2},Converted to jpg\n'.format(dirpath,file_name,extension))

            elif bool(re.search(r'\.(jpe?g|tiff?|png|gif|exif|bmp)$',file_name,re.IGNORECASE)):
                print('\t'+file_name+' is an image file, creating link')
                folder_name = os.path.split(target_dirpath)[1]
                link_name = '{0}_{1:0>5}.{2}'.format(folder_name,i+1,extension)
                link_path = os.path.join(target_dirpath,link_name)
                os.symlink(file_path, link_path)
                output_file.write('{0},{1},{2},Keep\n'.format(dirpath,file_name,extension))

            elif file_name=='report.csv':
                continue

            else:
                print("\tNot an image file, continue")
                output_file.write('{0},{1},{2},Continue\n'.format(dirpath,file_name,extension))
    output_file.close()


def convert_to_images(file_path,dst_path):
    pdf = open(file_path,'rb').read()

    startmark = b"\xff\xd8"
    startfix = 0
    endmark = b"\xff\xd9"
    endfix = 2
    i = 0

    njpg = 1
    while True:
        istream = pdf.find(b"stream", i)
        if istream < 0:
            break
        istart = pdf.find(startmark, istream, istream+20)
        if istart < 0:
            i = istream+20
            continue
        iend = pdf.find(b"endstream", istart)
        if iend < 0:
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(endmark, iend-20)
        if iend < 0:
            raise Exception("Didn't find end of JPG!")

        istart += startfix
        iend += endfix
        print ("\t\t JPG {0} from {1} to {2}".format(njpg, istart, iend))
        jpg = pdf[istart:iend]

        # Naming the file
        folder_name = os.path.split(dst_path)[1]
        save_name = "{0}_{1:0>5}.jpg".format(folder_name,njpg)

        save_file = os.path.join(dst_path,save_name)
        jpgfile = open(save_file, "wb")
        jpgfile.write(jpg)
        jpgfile.close()

        njpg += 1
        i = iend

if __name__=='__main__':
    start = time.time()
    main()
    total = time.time()-start
    sec = int(total%60)
    min = int((total//60)%60)
    hrs = int(total//3600)
    print('Process duration: {0:0>2}:{1:0>2}:{2:0>2}'.format(hrs,min,sec))
