# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 11:27:37 2015

@author: Duncan Parkes

Use the output from texcount to log how many words written on a latex document.
Output to a simple text file that can be plotted with your favourite plotting
software.

TODO:
    - Break up into functions
    - Run texcount from this script
    - Capture output from texcount run
    - Automatically plot with matplotlib?
    

"""


from datetime import datetime
import os
import subprocess


def run_texcount(folder, texfile):
    texcount = []
    os.chdir(folder)
    print os.getcwd()
    tex_count_command = "texcount -inc " + texfile
    print tex_count_command
#    subprocess.call(tex_count_command, shell=True)
    proc = subprocess.Popen(tex_count_command,stdout=subprocess.PIPE)
    while True:
      line = proc.stdout.readline()
      if line != '':
        #the real code does filtering here
        texcount.append(line.rstrip())
      else:
        break
    
    return texcount
def get_tex_total(countfile):
    block_of_lines = []

    with open(countfile) as input_data:
        # Skips text before the beginning of the interesting block:
        for line in input_data:
            if "total" in line.strip():  # Or whatever test is needed
                break
        # Reads text until the end of the block:
        for line in input_data:  # This keeps reading the file
            if line.strip() == 'Subcounts:':
                break
            print line
            block_of_lines.append(line.strip('\n'))  # Line is extracted (or block_of_lines.append(line), etc.)
            
    return block_of_lines
    
def logger(countfile):
    
    
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    block_of_lines = get_tex_total(countfile)
            
    #print block_of_lines
    
    headers = ['Date']
    values = [time_stamp]
    
#    print time_stamp
    
    for line in block_of_lines:
        (heading, value) = line.split(':')
        headers.append(heading)
        values.append(value)
    
    #print headers
    #print values
    
    
    
    output_file = "output.txt"
    with open(output_file,"a") as f:
        if os.stat(output_file).st_size == 0:
            f.writelines(",".join(map(str, headers)))
            f.writelines(",".join('\n'))
        f.writelines(",".join(map(str, values)))
        f.writelines(",".join('\n'))


tex_file = "thesis.tex"
folder = "Z:\\Backup\\thesis"
run_texcount(folder, tex_file)
countfile = "Z:\\Backup\\thesis\\texcount_output.txt"
logger(countfile)