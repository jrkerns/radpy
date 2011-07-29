#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described 
#in the PyQt GPL exception also apply
# 
# Author: Riverbank Computing Limited
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.
#
# RadPy is derived from the Enthought Acmelab workbench application example.
# Copyright (c) 2007 by Enthought, Inc.
# http://www.enthought.com
#
# Copyright (c) 2009-2011 by Radpy.
# http://code.google.com/p/radpy/  

# Standard library imports.
import sys

# Major package imports.
from PyQt4 import QtCore, QtGui

# Enthought library imports.
from enthought.traits.api import implements, Instance, List, Unicode

# Local imports.
from enthought.pyface.i_about_dialog import IAboutDialog, MAboutDialog
from enthought.pyface.image_resource import ImageResource
from enthought.pyface.dialog import Dialog


# The HTML displayed in the QLabel.
_DIALOG_TEXT = '''
<html>
  <body>
    <center>
      <table width="100%%" cellspacing="4" cellpadding="0" border="0">
        <tr>
          <td align="center">
          <p>
            <img src="%s" alt="">
          </td>
        </tr>
      </table>

      <p>
      %s<br>
      <br>
      Python %s<br>
      PyQt %s<br>
      Qt %s<br>
      </p>
      <p>
      Copyright &copy; 2009-2011 RadPy group<br>
      http://www.radpy.org
      </p>
  </center>
  </body>
</html>
'''


class AboutDialog(MAboutDialog, Dialog):
    """ The toolkit specific implementation of an AboutDialog.  See the
    IAboutDialog interface for the API documentation.
    """

    implements(IAboutDialog)

    #### 'IAboutDialog' interface #############################################

    additions = List(Unicode)

    image = Instance(ImageResource, ImageResource('about'))

    ###########################################################################
    # Protected 'IDialog' interface.
    ###########################################################################

    def _create_contents(self, parent):
        label = QtGui.QLabel()

        if parent.parent() is not None:
            title = parent.parent().windowTitle()
        else:
            title = ""

        # Set the title.
        self.title = "About %s" % title

        # Load the image to be displayed in the about box.
        image = self.image.create_image()
        #path = self.image.absolute_path
        path = './radpy/images/about.png'
        # The additional strings.
        additions = '<br />'.join(self.additions)

        # Get the version numbers.
        py_version = sys.version[0:sys.version.find("(")]
        pyqt_version = QtCore.PYQT_VERSION_STR
        qt_version = QtCore.QT_VERSION_STR

        # Set the page contents.
        label.setText(_DIALOG_TEXT % (path, additions, py_version, pyqt_version, qt_version))

        # Create the button.
        buttons = QtGui.QDialogButtonBox()

        if self.ok_label:
            buttons.addButton(self.ok_label, QtGui.QDialogButtonBox.AcceptRole)
        else:
            buttons.addButton(QtGui.QDialogButtonBox.Ok)

        buttons.connect(buttons, QtCore.SIGNAL('accepted()'), parent, QtCore.SLOT('accept()'))

        lay = QtGui.QVBoxLayout()
        lay.addWidget(label)
        lay.addWidget(buttons)

        parent.setLayout(lay)

#### EOF ######################################################################

