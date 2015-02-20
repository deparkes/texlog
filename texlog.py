# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 11:27:37 2015

@author: Duncan Parkes

Use the output from texcount to log how many words written on a latex document.
Output to a simple text file that can be plotted with your favourite plotting
software.

TODO:
    - Capture output from texcount run
    - Automatically plot with matplotlib?
    - Have command line capability: input file, output file, optparser
    - Option to store more than just the total
    

"""


from datetime import datetime
import os
import subprocess
#
#class section:
#    def __init__(self):

def run_texcount(folder, texfile):
    """ Run texcount on a specified file in a specified directory.
        Output the standard texcount output
    """
    texcount = []
    os.chdir(folder)
    print os.getcwd()
    tex_count_command = "texcount -inc " + texfile
    print "Running: ", tex_count_command
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
    """ Extract relevant section of the texcount output.
        I couldn't figure out how to do exactly what I """
    IncludedLineLimit = 0    
    FilesTotalLineLimit = 0    
    extract1 = False
    extract2 = False
    block_of_lines = []
#    with open(countfile) as input_data:
    # Skips text before the beginning of the interesting block:
    for line in countfile:
#        print line
#        type(line)

        if "Included file:" in line.strip()[:20]:  # Or whatever test is needed
            extract1 = True       
        if extract1:
            print line
            IncludedLineLimit +=1 
        if IncludedLineLimit > 8:
            extract1 = False
            IncludedLineLimit = 0
            
        if "File(s) total:" in line.strip()[:20]:
            extract2 = True       
        if extract2:
            print line
            FilesTotalLineLimit +=1 
        if FilesTotalLineLimit > 8:
            extract2 = False
            FilesTotalLineLimit = 0              
            
#            if "Words in text" in line.strip()[:20]:
##            print line
#                extract = True
#            if 'Number of math displayed'  in line.strip()[:26]:
#                extract = False
#            elif extract:
#                print line
##            if not "total" in line.strip():
#                block_of_lines.append(line.strip())  # Line is extracted (or block_of_lines.append(line), etc.)
#        else:
#            break
    return block_of_lines
    
def logger(folder, tex_file):

    
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
#    if os.path.isfile(countfile):
#        with open(countfile) as input_data:
#            for line in input_data:
#                texcount.append(line.rstrip())
#    else:
    texcount = run_texcount(folder, tex_file)
    block_of_lines = get_tex_total(texcount)
            
    #print block_of_lines
    
    headers = ['Date']
    values = [time_stamp]
    
#    print time_stamp
    
    for line in block_of_lines:
        print line
        try:
            (heading, value) = line.split(':')
            headers.append(heading)
            values.append(value)
        except Exception as e:
            print "Problem with ", line
            print "Error:", e
    
    #print headers
#    print values
    
    
    output_file = "output.txt"
    with open(output_file,"a") as f:
        if os.stat(output_file).st_size == 0:
            f.writelines(",".join(map(str, headers)))
            f.writelines(",".join('\n'))
            
        f.writelines(",".join(map(str, values)))
        f.writelines(",".join('\n'))


tex_file = "thesis.tex"
folder = "Z:\\Backup\\thesis"
#run_texcount(folder, tex_file)
#countfile = "Z:\\Backup\\thesis\\texcount_output.txt"
logger(folder, tex_file)