# Introduction #

RadPy allows you to plot scans and take actions to modify the plotted data.


# Plotting 1D scans #

To plot a single scan, either double click on the scan or right click on the scan and select 'Add to plot'.

![http://radpy.googlecode.com/svn/wiki/images/Edit_Beam.png](http://radpy.googlecode.com/svn/wiki/images/Edit_Beam.png)

Multiple scans can be plotted by right clicking on a branch in the Tree View and selecting 'Add all to plot'.

![http://radpy.googlecode.com/svn/wiki/images/Edit_multi.png](http://radpy.googlecode.com/svn/wiki/images/Edit_multi.png)

Plots are added to plot windows in the middle of RadPy's workspace.  Multiple plot windows can be open at the same time.  To add a new plot window, go to the File menu and select 'New Plot', or click on the new plot icon in the toolbar.  You can switch to a different plot window by left clicking on its tab at the top.  If there are multiple plot windows open, any new scans plotted will be added to the currently selected window.

Each plot window can only contain one type of scan (depth dose, inplane or crossplane).  If the currently selected plot window is a different type than the plot added, a new plot window will be created and the plot added to it.

Individual plots can be selected by left clicking on the plot itself or on its entry in the legend.  When a plot is selected, various parameters related to the scan (D50, Full Width Half Maximum, etc.) will appear in the parameters window.  These parameters are calculated by scripts in the \RadPy\Scripts directory and can be created by users.  See [Created Scripts](User.md) for details on how to create your own.

In addition, there are various actions that can be taken on the selected scan.  Examples of an action are smoothing or normalizing a scan.  These actions can appear as icons in the toolbar or as options under the 'Tools' menu.  Again, actions are in the 'Scripts' folder and can be created by users.  See [Created Scripts](User.md).



# Plotting a 3D Dicom-RT Dose file #

A three dimensional Dicom-RT Dose data set can be plotted by RadPy in a 3 orthogonal plane view.  When the data set is double clicked in the Tree View or 'Add to Plot' is selected, a new 3D plot window will be created.

![http://radpy.googlecode.com/svn/wiki/images/3d_plot.png](http://radpy.googlecode.com/svn/wiki/images/3d_plot.png)

The viewing plane sliders can be moved to adjust the plane plotted in each view and to update the box at the bottom of the view that gives the dose at the intersection of the viewing planes.