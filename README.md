# texlog
Log the 'texcount' wordcount output from your tex files.

Outputs to simple text files that can be plotted with your favourite plotting
software.

Data extracted from texcount:

	Date
	Included file
	Encoding
	Words in text
	Words in headers
	Words outside text (captions etc.)
	Number of headers
	Number of floats/tables/figures
	Number of math inlines,Number of math displayed

# Requirements

For texlog to work, you have to be able to run this: 

	'texcount -inc thesis.tex'

and have it run with out errors.

If you're using Windows, texcount is installed with Miktex.

# Usage 

	texlog.py tex_file.tex


The output is a series of text files for each of the consituent files of the tex document, and the total for the whole document.

Output to: 
	<tex_file_directory>/Logging/<tex_file_name>/



# Todo
- Further integration with thesisplotter.py to plot the output of the thesis.
