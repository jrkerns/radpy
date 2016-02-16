# Introduction #

From the Enthought [wiki](https://svn.enthought.com/enthought/wiki/EnvisageThree/Workbench.html):


> Views are primarily used to present information to the user to help them perform their current task.

> In an IDE application, views might be:
    * file tree
    * class outlines

Robert Kern wrote in a message on [Enthought-dev](https://mail.enthought.com/mailman/listinfo/enthought-dev):

> Views are persistent. They are always alive while the Workbench itself is, regardless of whether they are currently displayed or not. They should be written accordingly. They can modify the state of your multiple model objects, certainly. They just need to be able to handle having their model object being hotswapped out, or perhaps not having any model object at all (e.g. if the View responds to the user's current selection). Or their models need to be persistent throughout the lifetime of the WorkbenchWindow (e.g. if the View just views/configures a service that is part of the app structure itself and not your model objects). Typically they will connect to just such a persistent service and respond to changes there.



# Details #

A view window can be created by subclassing the Pyface View class and implementing the create\_control function.  For example, in the Beam Analysis plugin, the tree view is created like this:

```
from enthought.pyface.workbench.api import View 
...
class TreeView(View):

     def __init__(self, *args, **kwds):    
        View.__init__(self, *args, **kwds)
        self.widget = TreeWidget()

...

     def create_control(self, parent):                      
        return self.widget
```

The TreeWidget class is a subclass of PyQt's QTreeView and is implemented purely in PyQt.  In this sense, the pyface View class is just a wrapper around the PyQt code.

While this allows us to use PyQt code instead of TraitsGUI code, which is much more limited, there are some disadvantages.  The TreeWidget class uses a PyQt signal when a leaf is activated.  As far as I know, there is no way to connect this signal to the main RadPy application.  However, a TraitsGUI object could send a Traits event that could be watched by a handler in the main application (possibly?).

To add a view to a Plugin, you can add it to the Views List trait of the Plugin object.  In BeamAnalysis\_workbench\_plugin.py, the BeamAnalysisWorkbenchPlugin object has the following Trait initializer:

```
def _views_default(self):
        """ Trait initializer. """

        from radpy.plugins.BeamAnalysis.api import TreeView

        return [TreeView]
```

To add the view to a perspective, it must be added to the contents attribute of the Perspective object.

```
class BeamAnalysisPerspective(Perspective):
    # The perspective's name.
    name = 'Beam Analysis'

    # Should the editor area be shown in this perspective?
    show_editor_area = True

    # The contents of the perspective.
    contents = [
        PerspectiveItem(id='TreeView', position='right', relative_to='ScanPlot')
    ]
```