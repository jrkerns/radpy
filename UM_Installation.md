# Introduction #

RadPy can be installed and run either by using a binary installer or by downloading the source.

# Windows #

## Binary Installer ##

The latest version of the RadPy binary installer for Windows is available in the [Downloads](http://code.google.com/p/radpy/downloads/list) section.  If downloaded and installed, no further software is needed.

Note:  Currently the binary version of RadPy only contains the core Beam Analysis plugin cannot read the source version of other plugins.  If you want to use other plugins, you must install the source version as described below.

The installer will create shortcuts in the Start menu and on the desktop (if that option is selected).  Double click either shortcut to start RadPy.

## Source Installation ##

The source code for RadPy is available in the [Downloads](http://code.google.com/p/radpy/downloads/list) section in tarred, gzipped form (extension .tar.gz)  It can be extracted with several Windows based programs (one of which is [7-zip](http://www.7-zip.org/).  Once downloaded and extracted, the source code can be installed in any folder.

To use the source version, the Python interpreter and supporting libraries must be installed on your computer.  The easiest way to install the [Requirements](Requirements.md) on Windows is to install the [Python x,y](http://www.pythonxy.com) distribution.  In particular, the following Python x,y modules need to be installed:

  * Python
  * PyQt
  * NumPy
  * SciPy
  * ETS (version 3.6 or earlier)
  * pydicom

These modules can be found [here](http://www.pythonxy.com/standard.php).

In addition, the [lxml](http://lxml.de/) XML parsing library must be installed.

To run the source version of RadPy, double click on the run.py file in the source directory or run it with the Python interpreter.

# MacOS #

A disk image of the binary version of RadPy is available on the downloads page.  To install, download the disk image, open it and drag the RadPy folder to your Applications folder.

# Linux #

In order to run the source version of RadPy on a debian based system, the following packages must be installed (via sudo apt-get install or through a package manager program):

  * python-scipy
  * python-lxml
  * python-qt4
  * python-dev
  * python-qt4-gl
  * python-configobj
  * swig

The following libraries are needed to download and compile the Enthought Tool Suite:

  * git-core
  * libx11-dev
  * mesa-common-dev
  * libglu1-mesa-dev
  * libqt4-opengl-dev
  * python-qt4-gl

The Enthought Tool Suite can then be installed using the directions found [here](http://code.enthought.com/source/).