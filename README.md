# texlog
Use the output from texcount to log how many words written on a latex document.
Output to a simple text file that can be plotted with your favourite plotting
software.

For it to work, you have to be able to type 'texcount -inc thesis.tex'
and have it run with out errors.

Sections such as chapters, introduction, etc. need to be in their own folder,
other wise this will likely crash.

The output is a text file of the various texcount outputs for each file, and
the total for the whole document.


# Known Issues
- Fails if run from IDLE due to subprocess error.
