# Introduction #

RadPy has the ability to look within a set of 1D scans and find scans which match the currently plotting scan according to a set of user specified criteria.  It can also extract a matching 1D profile from a 3D Dicom-RT Dose
data set.

# Finding Matching Profiles #

To find the scans in a reference data set that match a particular scan, first load the scan and plot it in the RadPy plot window.  Open your reference data set and right click on a branch in the Tree View.  (RadPy will only look for scans under the branch you choose.)  Choose 'Add matching beams'.  This will pull up the 'Parameters to match' dialog.

![http://radpy.googlecode.com/svn/wiki/images/parameters_to_match.png](http://radpy.googlecode.com/svn/wiki/images/parameters_to_match.png)

Move the parameters you want to match into the right hand window of the dialog and press 'OK'.  All beams in the reference data set will be tested to see if they match the plotted scans according to those parameters.  If they match they will be plotted in the current scan window.

If the reference data set is a 3D Dicom dataset, RadPy will test all parameters except for 'Depth' and 'Scan Type'.  If other selected parameters match, RadPy will calculate a 1D profile at the proper depth and in the proper direction via interpolation.  If the depth of the scan exceeds the maximum depth of the 3D data set, an error will occur.

# Example #

In the sample data set, open the 'Test1.rfb' and the 'RD.10x10-anon.dcm' files.  'Test1.rfb' is a data set consisting of 1D profiles for 6X and 18X energies for various filed sizes.  'RD.10x10-anon.dcm' is a 3D Dicom dataset for a 10x10 field with 6X energy.

Open the 'Test1' tree and find a 6X, 10x10 Crossplane profile at a depth of 5 cm.  Plot it in a new RadPy plot window.

Right click on the 'RD.10x10-anon' tree and select 'Add matching beams'.

![http://radpy.googlecode.com/svn/wiki/images/Match_example_1.png](http://radpy.googlecode.com/svn/wiki/images/Match_example_1.png)

In the 'Parameters to Match' dialog select 'Depth', 'Field Size', 'Scan Type' and 'Energy'.  Click 'Ok'.

![http://radpy.googlecode.com/svn/wiki/images/Match_example_2.png](http://radpy.googlecode.com/svn/wiki/images/Match_example_2.png)

A new crossplane profile at a depth of 5 cm will be plotted in the plot window.  Since the Dicom dose file is in units of absolute dose, both plots will have to be normalized to compare them (click on each plot and click the 'Quick Normalize' button on the toolbar).

![http://radpy.googlecode.com/svn/wiki/images/Match_example_3.png](http://radpy.googlecode.com/svn/wiki/images/Match_example_3.png)