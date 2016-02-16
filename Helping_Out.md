# Introduction #

There are many areas in which you can contribute to the RadPy project, most of which do not require any programming knowledge.


# Helping Out #

## Documentation ##

Let's face it.  No one wants to write documentation.  Therefore, anyone who makes the effort to better document a portion of RadPy will have the thanks of a grateful nation of medical physicists.  There is no need to know how the internal code of RadPy works.  A tutorial that explains how to perform various tasks will be of great help to many users who just want to know how to do "X".  Write one up and send it to a project owner and we'll put it in the wiki.

## File Formats ##

One of the goals of the RadPy project is to create open formats for the storage of data.  In order to accomplish this, RadPy needs to be able to read files of all types.  Any knowledge of the internal structure of various file types will be gratefully appreciated.  In particular, the Beam Analysis plugin needs to be able to read Omnipro and PTW beam data files.  Currently, RadPy can read some Omnipro (version 6 or later) .RFB files , but still gets errors on some files.  If you receive an error attempting to read an .RFB file, please send the file to flounder.sdt@gmail.com.  There is no current support for Mephysto files.  Any knowledge of the Mephysto file format would be greatly appreciated.

## Unit Tests ##

Unit testing is the automated validation of software results.  This is very important as small changes to code can cause errors in data analysis routines that may go undetected.  RadPy uses the Python [unittest](http://docs.python.org/library/unittest.html) module.  The RFBTest.py module in the radpy/src/plugins/BeamAnalysis/view/RFB directory is an example.

Any code that modifies or analyzes data should have a unit test.  Eventually a unit testing framework for the entire RadPy suite will be created.  Unit tests for individual plugins or modules should tie into this framework.

## Fixing Bugs/Adding Features ##

Any patches that add features or fix bugs are always welcome.  The [Issues list](http://code.google.com/p/radpy/issues/list) is a good place to start to find areas that need improvement.  To submit a patch, you must first create a patch file.  There are several utilities that can create a patch file, but the easiest way is probably to use your subversion client.  The [TortoiseSVN](TortoiseSVN.md) and [Subclipse](Subclipse.md) pages have information on how to create a patch file with your changes.

## Becoming a Core Developer ##

Once you have been an active developer for some time and have demonstrated an ability to generate top quality patches, you can be accepted as a core developer.  This will give you the ability to make changes directly to the RadPy source tree.

## Developing Plugins ##

The core RadPy application contains mostly GUI code.  At heart, it is an attempt to make writing plugins for the Enthought workbench application easier for non-programmers.  The code to accomplish actual medical physics tasks is meant to come from plugins.  As such, developing new plugins or improving existing plugins for RadPy is probably the most important thing you can do to help the RadPy effort.  The RadPy Plugin Guide (coming soon!) is the best place to start.