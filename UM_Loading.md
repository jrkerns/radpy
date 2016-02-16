# Introduction #

RadPy currently can read beam data in RFB, Dicom or BDML formats.

# Opening a file #

To open an RFB file, click on the Open File button on the Toolbar or on the Open File option in the File Menu.  This will open a file dialog (set by default to open in the /Data directory in the RadPy installation folder).  Files with the extensions .rfb, .dcm or .xml will be shown.  Click on the desired file.

The profiles contained within the file will show up in a tree structure in the Tree View window to the right.
![http://radpy.googlecode.com/svn/wiki/images/TreeView2.png](http://radpy.googlecode.com/svn/wiki/images/TreeView2.png)

Each profile will be grouped within the tree by the following parameters (in descending order): file name, machine, energy, wedge type and field size.  If another file is opened, those scans will appear in a new tree under that file name.

![http://radpy.googlecode.com/svn/wiki/images/TreeViewMulti.png](http://radpy.googlecode.com/svn/wiki/images/TreeViewMulti.png)

To close a file, right click on the file name in the tree menu and select Close from the context menu.  That tree will disappear from the Tree View.

![http://radpy.googlecode.com/svn/wiki/images/Close.png](http://radpy.googlecode.com/svn/wiki/images/Close.png)

# Opening a directory #

To open every file within a directory (and subdirectories) go to the File menu and select 'Open Directory'.  RadPy will attempt to open any file that has a '.rfb', '.dcm' or '.xml' extension.  All of the data will be included in the same tree in the Tree View.

# Specific file type notes #


## RFB ##

In order to be able to read the data in an RFB file, the file must only contain inplane, crossplane and depth dose profiles for either electrons or photons.  Any TMR, absolute dose, 2D image, point-to-point scan, diagonal scan or any other data the file contains will prevent RadPy from reading it.

## Dicom-RT ##

When a Dicom RTDose file is selected in the open menu, RadPy will search its directory for a corresponding RTPlan file.  An RTPlan file corresponds if it has the same SOP Instance UID tag as the RTDose file.
If an RTPlan file is not located, the Dose file will not be loaded.

## BDML ##

All XML files opened will be validated against the BDML schema.  If it is not a valid BDML file, it will not be opened.  You can find the BDML schema at http://www.radpy.org/BDML/BDML.xsd or in the RadPy program directory under /dist/radpy/plugins/BeamAnalysis/BDML.