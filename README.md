# texlog
Use the output from texcount to log how many words written on a latex document.
Outputs to simple text files that can be plotted with your favourite plotting
software.

# Requirements

For texlog to work, you have to be able to type 

	'texcount -inc thesis.tex'

and have it run with out errors.

If you're using Windows, texcount is installed with Miktex.

# Usage 

	texlog.py tex_file.tex


The output is a series of text files for each of the consituent files of the tex document, and the total for the whole document.

Output to: 
	<tex_file_directory>/Logging/<tex_file_name>/

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

# Todo
- Further integration with thesisplotter.py to plot the output of the thesis.
