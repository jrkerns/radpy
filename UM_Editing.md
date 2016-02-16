# Introduction #

The BDML tags associated with a particular scan can be edited and the changes can be saved into a file in BDML format.


# Editing Scans #

To edit the metadata for a particular scan, right click on it and choose 'Edit beam parameters' from the context menu.

![http://radpy.googlecode.com/svn/wiki/images/Edit_Beam.png](http://radpy.googlecode.com/svn/wiki/images/Edit_Beam.png)

This will bring up the 'Edit properties' dialog where the beam metadata can be viewed and edited.

![http://radpy.googlecode.com/svn/wiki/images/Edit_properties.png](http://radpy.googlecode.com/svn/wiki/images/Edit_properties.png)

# Editing Multiple Scans #

If you right click on a branch of the tree that has multiple scans, you can make changes to the metadata for scans contained within that branch.  Right click on the branch and select 'Edit parameters for all beams'.

![http://radpy.googlecode.com/svn/wiki/images/Edit_multi.png](http://radpy.googlecode.com/svn/wiki/images/Edit_multi.png)

The 'Edit properties' dialog will come up.  Any parameter that is the same for all scans in that branch will appear in the dialog.  If there are parameters which differ among the scans, the box for that parameter will be blank. In the following image, the 10x10 branch has been selected.  There are crossplane scans at various depths, an inplance scan and a depth dose contained within that branch.  Since the start and stop positions will differ for all of those scans, those boxes are blank.  However, since they share the same isocenter, those boxes show the values.

![http://radpy.googlecode.com/svn/wiki/images/Edit_multi_properties.png](http://radpy.googlecode.com/svn/wiki/images/Edit_multi_properties.png)

Any edits that are made and then accepted in the dialog will be changed for every scan in that branch.  This includes boxes that are initially blank.  For example, if there was a branch that contained scans of different field sizes, the jaw position boxes would be blank.  If you entered values for, say, a 10x10 field, all of the scans in that branch would be changed to be 10x10.

# Saving Files #

To save a file into BDML format, click on the tree you want to save in the Tree View so that it is highlighted, go to the File menu and select 'Save File'.  Currently, you can only save trees at the top level (the file name or directory name level).  You cannot select a particular sub branch and only save that part of the tree.