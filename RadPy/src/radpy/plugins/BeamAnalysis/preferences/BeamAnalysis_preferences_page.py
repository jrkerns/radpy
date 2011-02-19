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
from enthought.preferences.ui.api import PreferencesPage
from enthought.traits.api import Bool, Color, Int, Float, Font, Str, List
from enthought.traits.ui.api import View


class BeamAnalysisPreferencesPage(PreferencesPage):
    """ The preferences page for the RadPy workbench. """

    #### 'PreferencesPage' interface ##########################################

    # The page's category (e.g. 'General/Appearance'). The empty string means
    # that this is a top-level page.
    category = 'General'

    # The page's help identifier (optional). If a help Id *is* provided then
    # there will be a 'Help' button shown on the preference page.
    help_id = ''
    
    # The page name (this is what is shown in the preferences dialog.
    name = 'Beam Analysis'

    # The path to the preference node that contains the preferences.
    preferences_path = 'radpy.plugins.BeamAnalysis'

    #### Preferences ##########################################################

#    # Width.
#    width = Int(100)
#
#    # Height.
#    height = Int(200)
#
#    # Ratio.
#    ratio = Float(0.1)
#    
#    # Background color.
#    bgcolor = Color('red')
#
#    # Text font.
#    font = Font('helvetica')
    
    match_params = List(['Energy','Scan Type','Field Size'])
    
    #### Traits UI views ######################################################

    trait_view = View('match_params')

#### EOF ######################################################################
