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
# Copyright (c) 2009 by Radpy.
# http://code.google.com/p/radpy/  


# Enthought library imports.
from enthought.pyface.workbench.api import Perspective, PerspectiveItem


class BeamAnalysisPerspective(Perspective):
    # The perspective's name.
    name = 'Beam Analysis'

    # Should the editor area be shown in this perspective?
    show_editor_area = True

    # The contents of the perspective.
    contents = [
        #PerspectiveItem(id='scanplot.plot2d'),
        PerspectiveItem(id='TreeView', position='right', relative_to='ScanPlot')
    ]
    
#### EOF ######################################################################
