# Windows #

## Requirements ##

The easiest way to install the [Requirements](Requirements.md) on Windows is to install the [Python x,y](http://www.pythonxy.com) distribution.  In particular, the following Python x,y modules need to be installed:

  * Python
  * PyQt
  * NumPy
  * SciPy
  * ETS (version 3.6 or earlier)
  * pydicom

These modules can be found [here](http://www.pythonxy.com/standard.php).

In addition, the [lxml](http://lxml.de/) XML parsing library must be installed.

## RadPy ##
Once the requirements are installed, a source archive can be downloaded from the [downloads](http://code.google.com/p/radpy/downloads/list) page, or the latest development version can be checked out from the subversion repository.

### Source archive ###
Unzip the source archive to any directory, making sure to maintain the subfolder structure (this should be an option on your unzipping application).  To run RadPy, double click on the run.py file in the RadPy/src/ folder.

### Subversion repository ###
General instructions for checking out the latest source revision can be found at [this page](http://code.google.com/p/radpy/source/checkout).  There are many subversion clients available for Windows.  One good one is [TortoiseSVN](http://tortoisesvn.net/downloads).  TortoiseSVN is a Windows shell extension, and is integrated directly into Windows Explorer.  To checkout the source using Tortoise SVN, open an Explorer window and browse to the folder you want to download the code into.  Right click on the folder and select 'SVN Checkout...'.  In the 'URL of repository' window enter "http://radpy.googlecode.com/svn/trunk/".  The source code will then be downloaded.

# MacOS #

# Linux #