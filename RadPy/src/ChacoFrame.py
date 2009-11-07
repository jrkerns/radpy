from PyQt4 import QtGui


class ChacoFrame(QtGui.QWidget):
    def __init__ (self, parent, **kw):
        QtGui.QWidget.__init__(self)

        # Create the subclass's window
        self.plot_window = self._create_window()

        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(self.plot_window.control)

        self.setLayout(layout)

        if 'size' in kw:
            self.resize(*kw['size'])

        if 'title' in kw:
            self.setWindowTitle(kw['title'])

        self.show()

    def _create_window(self):
        "Subclasses should override this method and return an enable.Window"
        raise NotImplementedError