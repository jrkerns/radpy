RadPy is a project to simplify analysis of data used in medical physics with an emphasis on radiation therapy.  Version 0.10 will be released under the BSD license.  There are two main design goals for RadPy:

1.  The creation of a standard format for the storage of data where none currently exists.  The main impetus for this goal is the proliferation of formats for the storage of scanning profiles of radiation therapy beams.  Right now it is very difficult to compare profiles between systems from different vendors.  RadPy will hopefully act as a bridge between systems for profile and other data.

2.  A tool for the visualization and analysis of data.  Ultimately the goal is for RadPy to not only analyze beam profile data but any data written in a readable format (e.g. DICOM).  This could include tasks such as IMRT QA, 3D image registration, etc.

RadPy is in pre-alpha status, meaning that several critical features are missing.  As of now, RadPy has not been approved for clinical use by the FDA or any other regulatory body.  It is provided for research purposes only.

# Latest Updates #

3/12/12 **OSX Version Released** A disk image is now available on the downloads page that contains a MacOS binary version of RadPy.  There are also detailed instructions in the [User's Manual](http://code.google.com/p/radpy/wiki/UM_Installation) on how to configure a debian based linux system to run the source version of RadPy.  The next job is to separate out beam data reading and writing functionality into a stand alone python module.

11/26/11 **User's Manual Complete** The first (brief) draft of the [User's Manual](http://code.google.com/p/radpy/wiki/Users_Manual) is complete.  Tutorials will follow eventually, but next up is compatibility with Enthought Tool Suite v4.0.  This will hopefully allow for a OSX and Linux version to be released soon after.

10/21/2011 **RadPy 0.1.1 Release** Fixes an issue with installation on some Windows XP computers (and possibly Vista and 7) where the wrong .dll files were bundled with RadPy.

9/28/2011 **RadPy 0.1 Release**  The first Windows binary release of Radpy, [version 0.1](http://code.google.com/p/radpy/downloads/detail?name=RadPy_setup_0.1.win32.exe&can=2&q=), is now available for download.

9/6/2011 - With the 100th commit to the source repository, RadPy is nearing readiness for the first binary release.  I expect a Windows binary version to be ready by the end of this month with MacOS and Linux versions following.


# Contributing #
There are many ways to help out with RadPy.

  * File a bug report or feature request on the [Issues](http://code.google.com/p/radpy/issues/list) page.
  * Join the conversation on the [RadPy users](http://groups.google.com/group/radpy-users) mailing list.
  * Contribute documentation or source code.  (Details can be found on the [Helping Out](Helping_Out.md) page).