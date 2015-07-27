# texlog
Log the 'texcount' wordcount output from your tex files.

Outputs to simple text files that can be plotted with your favourite plotting software.

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
[Python 2.7](https://www.python.org/downloads/) (it probably works on Python 3.x, but this is currently untested)

Perl - [texcount itself requires perl](http://tex.stackexchange.com/questions/158796/miktex-and-perl-scripts-and-one-python-script). Try the community version of [Active Perl](http://www.activestate.com/activeperl).

[More information about installing texcount](http://app.uio.no/ifi/texcount/howto.html)


# Installation
Either use pip:

	pip install texlog

Or [download the zip package](https://github.com/deparkes/texlog/releases).

In either case, add texlog folder to your path environment variable.

### Windows Users
Windows tends to have a problem that makes it difficult to run python scripts with arguments at the command line. 

If you are using windows you may need to modify one or both of the following registry settings:

Set the

	HKEY_CLASSES_ROOT\Applications\python26.exe\shell\open\command

and

	HKEY_CLASSES_ROOT\py_auto_file\shell\open\command

keys to:

	 "C:\Python26\python26.exe" "%1" %*

[More information about registry keys](http://stackoverflow.com/questions/1934675/how-to-execute-python-scripts-in-windows)
### Using Config Files
If you do have problems with command line arguments texlog will give you the option to create a configuration file containing the name of the tex file you wish to log.

The configuration file will be created in your 'home' or 'my documents' folder as
	
	home/texlog/texlog.ini

The configuration file looks like this:

	[texlog]
	tex_file = YourTextFile.tex

Edit the 'YourTextFile.tex' to your tex file - either the file name or full path, depending on where you run texlog from.

# Usage
The default usage is:

	texlog.py tex_file.tex

The output is a series of text files for each of the consituent files of the tex document, and the total for the whole document.

Output to: 
	DIRECTORY/Logging/TEXFILE/



# Todo
- Further integration with thesisplotter.py to plot the output of the thesis.
- Improve windows workaround to make it easier to run from the command line e.g. use a config file containing the name/directory of the file you want to run on.
