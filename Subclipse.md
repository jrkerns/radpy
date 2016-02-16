# Introduction #

Subclipse is a [Subversion](Subversion.md) client for the Eclipse IDE.  Here is how to set it up to work with the RadPy [Subversion repository](http://code.google.com/p/radpy/source/list).


# Details #

## Checking out the source ##
A good tutorial can be found [here](http://blog.msbbc.co.uk/2007/06/using-googles-free-svn-repository-with.html).

The [Eclipse](http://eclipse.org/) IDE is a very useful tool for working with source code.  It is plugin based and has the same View/Editor/Perspective interface that RadPy does.  While Eclipse is designed for Java, there is a Python plugin called [Pydev](http://pydev.org/).  You can install these separately, or install [Python(x,y)](http://www.pythonxy.com) which installs both by default.  To install Subclipse, follow the directions found [here](http://subclipse.tigris.org/servlets/ProjectProcess?pageID=p4wYuA).

Open Eclipse.  Make sure you are in the Pydev perspective.  (Usually you can switch perspectives by clicking on the buttons in the upper right corner).  The package explorer window is on the left by default.  Right click in that window and select 'New/Other...'.  This will open a window titled 'Select a wizard'.  Under the SVN branch of the tree will be a wizard that says 'Checkout Projects from SVN'.  Select it and click 'Next'.

The next window will be titled 'Select/Create Location'.  Select 'Create a new repository location' and click 'Next'.  In the space for a URL put 'http://radpy.googlecode.com/svn'.  (If you have commit access and want to be able to commit your changes to the repository put 'https://radpy.googlecode.com/svn'.)  Click 'Next' to proceed to the folder tree.  Open the 'trunk' branch of the tree and select the 'RadPy' directory.  Click 'Next'.

Select 'Check out as a project configured using the New Project Wizard' and select 'Finish'.  In the 'Select a wizard' window, open the Pydev branch and select 'Pydev Project'.  Click 'Next'.  Give the project a name and select 'Finish'.

## Source Operations ##

To update, in the Pydev perspective, right click on the RadPy project and go to 'Team/Update to Head'.

To create a patch, right click on the RadPy project and go to 'Team/Create patch'.

To commit changes, go to the Team Synchronize perspective.  Depending on the changes that have been made, you may have to resolve conflicts with changes other users have made.