# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 11:27:37 2015

@author: Duncan Parkes

Use the output from texcount to log how many words written on a latex document.
Output to a simple text file that can be plotted with your favourite plotting
software.

For it to work, you have to be able to type and 'texcount -inc <yourfile>'
and it to work.

Sections such as chapters, introduction, etc. need to be in their own folder,
other wise this will likely crash.

The output is a text file of the various texcount outputs for each file, and
the total for the whole document.

TODO:
    - Automatically plot with matplotlib?
    - Have command line capability: input file, output file, optparser
    - Option to store more than just the total
    

"""


from datetime import datetime
import os
import subprocess

class section(object):
    def __init__(self,filename):
        self.filename = filename
        self.block_of_lines = []
        self.data = []
        self.time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    
    def get_data(self):
        headers = ['Date']
        values = [self.time_stamp]
        for line in self.data:
            try:
                (heading, value) = line.split(':')
                print heading
                headers.append(heading.replace(',',''))
                values.append(value)
            except Exception as e:
                print "Problem with ", line
                print "Error:", e    
        return (headers,values)
    
    
def run_texcount(folder, texfile):
    """ Run texcount on a specified file in a specified directory.
        Output the standard texcount output
    """
    texcount = []

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
    ExtractList = []
#    with open(countfile) as input_data:
    # Skips text before the beginning of the interesting block:
    for line in countfile:
#        print line
#        type(line)

        if "Included file:" in line.strip()[:20]:  # Or whatever test is needed
            extract1 = True     
            (label, filename) = line.split(':')
            filename = os.path.dirname(filename).replace(' ./','')
            ExtractSection = section(filename)
#            print ExtractSection.filename            
        if extract1:
#            print line
            ExtractSection.data.append(line.strip())  # Line is extracted (or block_of_lines.append(line), etc.)
            IncludedLineLimit +=1 
        if IncludedLineLimit > 8:
            extract1 = False
            IncludedLineLimit = 0
            ExtractList.append(ExtractSection)  
        
        if "File(s) total:" in line.strip()[:20]:
            extract2 = True   
            (label, filename) = line.split(':')
            filename = 'Total'
            ExtractSection = section(filename)
#            print ExtractSection.filename            
        if extract2:
#            print line
            ExtractSection.data.append(line.strip())  # Line is extracted (or block_of_lines.append(line), etc.)
            FilesTotalLineLimit +=1 
        if FilesTotalLineLimit > 8:
            extract2 = False
            FilesTotalLineLimit = 0              
            ExtractList.append(ExtractSection)      

    return ExtractList
    
def logger(folder, tex_file, output_folder):

    texcount = run_texcount(folder, tex_file)
    ExtractList = get_tex_total(texcount)

    print "Sections found:"    
    for section in ExtractList:
        print section.filename
        (headers, values) = section.get_data()
        output_file = output_folder + '/' + section.filename + '.txt'
        with open(output_file,"a") as f:
            if os.stat(output_file).st_size == 0:
                f.writelines(",".join(map(str, headers)))
                f.writelines(",".join('\n'))            
            f.writelines(",".join(map(str, values)))
            f.writelines(",".join('\n'))


tex_file = "thesis.tex"
folder = "Z:\\Backup\\thesis"
output_folder = "./Logging"

os.chdir(folder)

if not os.path.exists(output_folder):
    os.mkdir(output_folder)
    
logger(folder, tex_file, output_folder)