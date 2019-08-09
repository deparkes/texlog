# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 11:27:37 2015

@author: Duncan Parkes

For it to work, you have to be able to type and 'texcount -inc <yourfile>'
and it to work.

Sections such as chapters, introduction, etc. need to be in their own folder,
other wise this will likely crash.

The output is a text file of the various texcount outputs for each file, and
the total for the whole document.

TODO:
    + Automatically plot with matplotlib? - see thesisplotter.py
    - Have command line capability: input file, output file, optparser
    - Option to store more than just the total
"""


from datetime import datetime
import os
import subprocess
import argparse
import sys
import configparser as configparser


def main():
    """
    Use the output from texcount to log how many words written on a latex document.
    Output to a simple text file that can be plotted with your favourite plotting
    software.
    Looks for file "thesis.tex" in the directory containing texlog.py

    Output data files to "./Logging"
    """
    parser = argparse.ArgumentParser(description='Log word count of tex files.')
    parser.add_argument('tex_file', nargs='?', help='Target tex file', action="store")

    try:
# First try to read the file name from the arguments
# This can pose a problem in windows, especially
        args = parser.parse_args()

        tex_file = args.tex_file
        # make sure there is something there with len()
        # This will fail if there is the problem with windows not accepting
        # filenames.
        len(tex_file)
    except:
        tex_file = create_config()

    folder = os.path.dirname(os.path.realpath(tex_file))
    #print("folder is: " + folder)
    #print("tex_file is: " + tex_file)
    #os.path.dirname(os.path.realpath(__file__))
    os.chdir(folder)

    output_folder = os.path.abspath(folder + '/' + "Logging" + '/' +
                                    os.path.splitext(os.path.basename(tex_file))[0])
    #print("Output To: " + output_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    logger(folder, tex_file, output_folder)


def create_config():
    """
    If there are problems with reading the file from the commandline ask the 
    user if they want to create a file to store the target file in.
    Output the name of the file they type in.
    Save the file name to a config file.
    """

    print("There was a problem reading the file from the command line")
    print("Attempting to load file from config file")
    config_parse = configparser.SafeConfigParser()
    try:
        # Attempt to make ini file in the texlog folder
        texlog_dir = os.path.expanduser("~") + '/' + 'texlog'
        if not os.path.exists(texlog_dir):
            os.makedirs(texlog_dir)

        ini_file = texlog_dir + '/' + 'texlog.ini'
        print("config file created in your home/my documents folder")
    except:
        # If there's a problem, put the file in the directory it was run from
        ini_file = 'texlog.ini'
        print("config file created in current directory")

    load_file_ok = False
    while not load_file_ok:
        try:
            # Try to read file from config file
            config_parse.read(ini_file)
            tex_file = config_parse.get('texlog', 'tex_file')
            print(("Loaded file: " + tex_file))
            load_file_ok = True
        except:
            # If there is a problem, create a new config file and ask for the
            # filename to operate on
            with open(ini_file, 'w') as config_file:
                print("File load failed")
                tex_file = input("Type filename for texfile here: ")
                config_parse.add_section('texlog')
                config_parse.set('texlog', 'tex_file', tex_file)
                config_parse.write(config_file)
                print((config_parse.get('texlog', 'tex_file')))

    return tex_file

class Section(object):
    """
    Your tex file may be comprised of different sections and chapters.
    Each chapter found by texcount as an 'include' will have its own output
    wordcount file.
    """
    def __init__(self, filename):
        self.filename = filename
        self.block_of_lines = []
        self.data = []
        self.time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    def get_data(self):
        """
        Extract the header and data information from the texcount output of
        each section.
        """
        headers = ['Date']
        values = [self.time_stamp]
        for line in self.data:
            try:
                (heading, value) = line.split(':', 1)
                print(heading)
                headers.append(heading.replace(',', ''))
                values.append(value)
            except Exception as problem:
                print("Problem with ", line)
                print("Error:", problem)
        return (headers, values)

def run_texcount(folder, texfile):
    """
    Run texcount on a specified file in a specified directory.
    Captures the standard texcount output.
    """
    texcount = []

    tex_count_command = "texcount -inc " + texfile
    print("Running: ", tex_count_command)
#    subprocess.call(tex_count_command, shell=True)
    proc = subprocess.Popen(tex_count_command, stdout=subprocess.PIPE, shell=True)
    while True:
        line = proc.stdout.readline()
        if line != '':
        #the real code does filtering here
            texcount.append(line.rstrip())
        else:
            break

    return texcount

def get_tex_total(countfile):
    """
    Extract relevant parts of the texcount output.
    """
    included_line_limit = 0
    files_total_line_limit = 0
    extract_included = False
    extract_total = False
    extract_root = False
    extract_list = []
#    with open(countfile) as input_data:
    # Skips text before the beginning of the interesting block:
    for line in countfile:
        print(line)
#        type(line)
#       Only some output lines are relevant. We have to treat the total words
#       as a special case.
        if "Included file:" in line.strip()[:20]:  # Or whatever test is needed
            extract_included = True
            (label, filename) = line.split(':')
            filename = os.path.dirname(filename).replace(' ./', '')
            extract_section = Section(filename)
#            print ExtractSection.filename
        if extract_included:
#            print line
#           Line is extracted to Section object
            extract_section.data.append(line.strip())
            included_line_limit += 1
#       Keep going until you reach the end of the headers/data for that section
        if included_line_limit > 8:
            extract_included = False
            included_line_limit = 0
            extract_list.append(extract_section)

        if "File(s) total:" in line.strip()[:20]:
            extract_total = True
            #print("split" + line.split(':', 1)[0])
            #print("split" + line.split(':', 1)[1])

            (label, filename) = line.split(':', 1)
            #print("problem with line" + line.strip()[:20])

            filename = 'Total'
            extract_section = Section(filename)
#            print ExtractSection.filename
        if extract_total:
#            print line
#           Line is extracted to Section object
            extract_section.data.append(line.strip())
            files_total_line_limit += 1
#       Keep going until you reach the end of the headers/data for that section
        if files_total_line_limit > 8:
            extract_total = False
            files_total_line_limit = 0
            extract_list.append(extract_section)
# Work-around for single-file documents      
        if "File:" in line.strip()[:20]:
            extract_root = True
            #print("split" + line.split(':', 1)[0])
            #print("split" + line.split(':', 1)[1])

            (label, filename) = line.split(':', 1)
            #print("problem with line" + line.strip()[:20])

            filename = 'RootFile'
            extract_section = Section(filename)
#            print ExtractSection.filename
        if extract_root:
#            print line
#           Line is extracted to Section object
            extract_section.data.append(line.strip())
            files_total_line_limit += 1
#       Keep going until you reach the end of the headers/data for that section
        if files_total_line_limit > 8:
            extract_root = False
            files_total_line_limit = 0
            extract_list.append(extract_section) 
# Need to add case for there being no included files
    return extract_list

def logger(folder, tex_file, output_folder):
    """
    Lists the sections of your document that have been found and word-counted
    by texcount. Saves output to txt file with the same name as section.
    """
    texcount = run_texcount(folder, tex_file)
    extract_list = get_tex_total(texcount)

    print("Sections found:")
    for section in extract_list:
        print(section.filename)
        (headers, values) = section.get_data()
        output_file = output_folder + '/' + section.filename + '.txt'
        with open(output_file, "a") as out_file:
            if os.stat(output_file).st_size == 0:
                out_file.writelines(",".join(map(str, headers)))
                out_file.writelines(",".join('\n'))
            out_file.writelines(",".join(map(str, values)))
            out_file.writelines(",".join('\n'))



if __name__ == "__main__":
    main()
    