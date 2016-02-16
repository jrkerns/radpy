# Introduction #

From the Enthought [wiki](https://svn.enthought.com/enthought/wiki/EnvisageThree/Workbench.html):
> Editors allow the user to manipulate data and objects to perform their current task.  Editors are really the focus of users attention with the views used to provide supporting information. Editors are grouped together geographically in what is known as the editor area.

In an IDE application, editors would contain the source code that a developer is currently working on.

Robert Kern wrote in a message on [Enthought-dev](https://mail.enthought.com/mailman/listinfo/enthought-dev):

> Editors are created and destroyed as you decide to edit new objects. The best way to think about this is to think of an IDE. We stole the View/Editor and the entire Workbench paradigm directly from Eclipse. You have persistent Views around the edges showing the project tree, debugger messages, etc. You don't have two project trees. But you can open many different files in their own Editors in the center of the Workbench. They are tied directly to the model that they are editing (for Eclipse, these are files) and will be destroyed when you close the Editor whereas Views just keep existing and will react to changing selections, the model currently being focused on, etc. They offer a few conveniences, like raising the focus of an existing Editor if the user requests to edit the same file instead of opening a duplicate Editor.

# Details #

Editor windows are created by calling the workbench.edit() method.  Views have a reference to the workbench application through the self.window.workbench attribute.  self.window also has an 'active\_editor ' attribute and an 'editors' attribute that is a list of all open editor windows.  For example, in the Beam Analysis plugin when a scan is double clicked, a new editor window is created and the scan added to the plot.

```
def activated(self, record):
        """ Adds the selected beam object to the active Chaco Plot editor.  If
        there is no active window, it creates one first.
        """
        
        label, beam = record
        if self.window.active_editor is not None:
            
            title = self.window.active_editor.obj.add_plot(label, beam)
            self.window.active_editor.name = title
        
        #If the tree view is undocked, there may not be an active editor,
        #even if one exists.   
        elif len(self.window.editors) > 0:   
            
            title = self.window.editors[-1].obj.add_plot(label, beam)
            self.window.editors[-1].name = title
        
        else:
            #Create new ChacoPlot editor window   
            plot = ChacoPlot()
            self.window.workbench.edit(plot, kind=ChacoPlotEditor)
            title = self.window.editors[-1].obj.add_plot(label, beam)
            self.window.editors[-1].name = title

```

The 'kind' keyword argument for the workbench.edit method passes a class to the workbench that defines the editor window.  This class can be subclassed from the TraitsUIEditor class.  The TraitsUIEditor displays whatever the traits\_view trait in the underlying object is set to display.  Here are the ChacoPlot and ChacoPlotEditor classes.

```
class ChacoPlotEditor(TraitsUIEditor):
        
    def _name_default(self):
        return "Scan Plot"


class ChacoPlot(HasTraits):

    plot = Instance(Component)
    name = 'Scan Plot'
    id = 'Scan Plot'
    traits_view = View(
                         Group(
                             Item('plot', editor=ComponentEditor(size=(400,300)),
                                  show_label=False),
                             orientation = "vertical"),
                         resizable=True, title="Test",
                        width=400, height=300, id='Scan Plot'
                         )
```

In this case, the only purpose in subclassing TraitsUIEditor was to override the default editor name to make it human readable.