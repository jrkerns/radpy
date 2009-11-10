#Force usage of Qt backend for chaco plotting library
from enthought.etsconfig.api import ETSConfig
ETSConfig.enable_toolkit = 'qt4'

#Python system imports
import os
import platform
import sys

#Major library imports
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy

#Program specific imports
import Model
import ChacoPlot
from RFB.hdf5 import load_multi_data

#COLUMNS is a list of fields for each branch of the 
#tree model (NEED TO ADD WEDGES, POSSIBLY OTHER FIELDS).
COLUMNS = ['File Name','Machine', 'Energy', 'Field Size']

__version__ = "0.0.1"


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.mdi = QMdiArea()

        #The tree model is held in a dockable window that can
        #be undocked or docked on the left or right.
        scan_dock_widget = QDockWidget("Scans", self)
        scan_dock_widget.setObjectName("ScanDockWidget")
        scan_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea|
                                         Qt.RightDockWidgetArea)
        
        #self.scan_tree is a widget to hold the tree model.
        self.scan_tree = TreeWidget(self)
        scan_dock_widget.setWidget(self.scan_tree)
        self.addDockWidget(Qt.RightDockWidgetArea, scan_dock_widget)
        
        self.setCentralWidget(self.mdi)
        
        #Create menu bar, file and window menus
        fileNewAction = self.createAction("&New...", self.fileNew,
                QKeySequence.New, "filenew", "Create a new scan")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen",
                "Open an existing scan")
        fileQuitAction = self.createAction("&Quit", self.close, "Ctrl+Q", 
                                           "filequit", "Close the Application")
        
        self.windowNextAction = self.createAction("&Next",
                            self.mdi.activateNextSubWindow, QKeySequence.NextChild)
        self.windowPrevAction = self.createAction("&Previous",
                            self.mdi.activatePreviousSubWindow,QKeySequence.PreviousChild)
        self.windowCascadeAction = self.createAction("Casca&de",
                            self.mdi.cascadeSubWindows)
        self.windowTileAction = self.createAction("&Tile",
                            self.mdi.tileSubWindows)
        self.windowRestoreAction = self.createAction("&Restore All",
                            self.windowRestoreAll)
        self.windowMinimizeAction = self.createAction("&Iconize All",
                            self.windowMinimizeAll)
        #No arrangeIcons equivalent for MDIArea?
#        self.windowArrangeIconsAction = self.createAction(
#                            "&Arrange Icons", self.mdi.arrangeIcons)
        self.windowCloseAction = self.createAction("&Close",
                            self.mdi.closeActiveSubWindow, QKeySequence.Close)
        
        self.fileMenu = self.menuBar().addMenu("&File")
        self.addActions(self.fileMenu, (fileNewAction,fileOpenAction))
        
        self.windowMenu = self.menuBar().addMenu("&Window")
        
        #Before window menu is shown, update the menu with the 
        #titles of each open window.
        self.connect(self.windowMenu, SIGNAL("aboutToShow()"),
                     self.updateWindowMenu)
        self.updateWindowMenu()
        
        #For future use.  This section will write the main window
        #size and position (possibly other settings) to a file,
        #so that reopening the program will restore those settings.
        settings = QSettings()
        size = settings.value("MainWindow/Size",
                              QVariant(QSize(1024, 768))).toSize()
        self.resize(size)
        position = settings.value("MainWindow/Position",
                                  QVariant(QPoint(0, 0))).toPoint()
        self.move(position)
        
        #If a scan is double-clicked (or enter pressed), retrieve
        #that scan's data.
        self.connect(self.scan_tree, SIGNAL("activated"),
                     self.activated)
        self.setWindowTitle("RadPy")
        self.fileNew()
        self.statusBar().showMessage("Ready...", 5000)
            
    def closeEvent(self, event):
        #Passes a close event from main window to all subwindows.
        
        self.mdi.closeAllSubWindows()
        
    def fileOpen(self):
        #Open a file and add it to the tree model.
        #Support for formats besides .rfb needs to be added here.
        
        #formats = ["*.rfb","*.asc","*.dcm",]
        fname = unicode(QFileDialog.getOpenFileName(self,
                            "Choose Scan", "./RFB/Unit Tests/",
                            "RFB Files *.rfb"))
                            #;;Dicom Files *.dcm;;Omnipro Export Files *.asc"))
        if fname:
            
            self.scan_tree.load(fname)
            
                
        
    def fileNew(self):
        #Creates a new window to display scans.
        scan_plot = QMdiSubWindow()
        scan_plot.setAttribute(Qt.WA_DeleteOnClose)
        scan_plot.setWidget(ChacoPlot.ChacoPlot(self))
        self.mdi.addSubWindow(scan_plot)
        scan_plot.show()
        scan_plot.setMinimumSize(QSize(400,300))
        
        
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        #Convenience function to create PyQt actions.
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
    
    def addActions(self, target, actions):
        #Add multiple actions to a menu
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
            
    def windowRestoreAll(self):
        for scan_plot in self.mdi.subWindowList():
            scan_plot.widget().showNormal()
            
    def windowMinimizeAll(self):
        for scan_plot in self.mdi.subWindowList():
            scan_plot.widget().showMinimized()
        
    def updateWindowMenu(self):
        #Creates a window menu with actions to jump to any open subwindow.
        self.windowMenu.clear()
        self.addActions(self.windowMenu, (self.windowNextAction,
            self.windowPrevAction, self.windowCascadeAction,
            self.windowTileAction, self.windowRestoreAction,
            self.windowMinimizeAction,
            #self.windowArrangeIconsAction, 
            None,
            self.windowCloseAction))
        scan_plots = self.mdi.subWindowList()
        if not scan_plots:
            return
        self.windowMenu.addSeparator()
        i = 1
        menu = self.windowMenu
        for plot in scan_plots:
            title = plot.windowTitle()
            if i == 10:
                self.windowMenu.addSeparator()
                menu = menu.addMenu("&More")
            accel = ""
            if i < 10:
                accel = "&%d " % i
            elif i < 36:
                accel = "&%c " % chr(i + ord("@") - 9)
            action = menu.addAction("%s%s" % (accel, title))
            self.connect(action, SIGNAL("triggered()"),
                         lambda w = plot: self.mdi.setActiveSubWindow(w))
            
            i += 1
                
                
                
    def picked(self):
        return self.treeWidget.currentFields()

    def activated(self, record):
        #Retrieves scan data from active item and plots it.
        #Adds plot to active sub window.
        label, beam = record
        
        x = self.mdi.activeSubWindow()
        self.mdi.activeSubWindow().widget().add_plot(label, beam)
        
class TreeWidget(QTreeView):
    #The window that organizes scans from opened files in a tree
    #structure.  The branches of the tree are defined by the 
    #COLUMNS global variable defined at the top of this file.
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)
        self.setSelectionBehavior(QTreeView.SelectItems)
        self.setUniformRowHeights(True)
        self.setSortingEnabled(True)
        
        model = Model.TreeModel(COLUMNS, self)
        
        #The ProxyModel acts as a wrapper to the underlying
        #tree model and enables custom sorting of tree columns.
        #For example, it can sort field sizes by equivalent 
        #square instead of strictly alphabetically.
        proxy = Model.ProxyModel(self)
        proxy.setDynamicSortFilter(True)
        proxy.setSourceModel(model)
        self.setModel(proxy)

        
        self.connect(self, SIGNAL("activated(QModelIndex)"),
                     self.activated)
        self.connect(self, SIGNAL("expanded(QModelIndex)"),
                     self.expanded)
        self.expanded()

    def load(self, filename):
        #Passes lists of scans to tree model class.
        nesting = len(COLUMNS)
        try:
            self.model().load(filename, nesting, COLUMNS)
        except IOError, e:
            QMessageBox.warning(self, "Server Info - Error",
                                unicode(e))
            
    def currentFields(self):
        return self.model().asRecord(self.currentIndex())


    def activated(self, index):
        self.emit(SIGNAL("activated"), self.model().asRecord(index))


    def expanded(self):
        for column in range(self.model().columnCount(QModelIndex())):
            self.resizeColumnToContents(column)



def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("RadPy Group")
    app.setOrganizationDomain("http://code.google.com/p/radpy")
    app.setApplicationName("RadPy")
    #app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()


main()
