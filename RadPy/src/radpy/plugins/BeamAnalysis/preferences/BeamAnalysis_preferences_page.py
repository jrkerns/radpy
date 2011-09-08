################################################################################
# Copyright (c) 2011, Stephen Terry and RadPy contributors
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are 
# met: 
# 
# 1. Redistributions of source code must retain the above copyright 
# notice, this list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright 
# notice, this list of conditions and the following disclaimer in the 
# documentation and/or other materials provided with the distribution. 
# 3. The name of Stephen Terry may not be used to endorse or promote products 
# derived from this software without specific prior written permission. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS 
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED 
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED 
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
# 
# RADPY IS NOT CERTIFIED AS A MEDICAL DEVICE.  IT IS INTENDED ONLY FOR RESEARCH 
# PURPOSES.  ANY OTHER USE IS ENTIRELY AT THE DISCRETION AND RISK OF THE USER.
################################################################################

# Enthought library imports.
from enthought.preferences.ui.api import PreferencesPage
from enthought.traits.api import Bool, Color, Int, Float, Font, Str, List
from enthought.traits.ui.api import View, Item, SetEditor, Group


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
    
    match_traits = List(['Energy','Scan Type','Field Size'])
    choices_dict = {'Energy':'BeamDetails_Energy',
                   'Field Size':'field_size',
                   'Scan Type':'scan_type',
                   'SSD':'BeamDetails_SSD',
                   'Wedge Angle':'BeamDetails_Wedge_Angle',
                   'Applicator':'BeamDetails_Applicator',
                   'Linac Model':'BeamDetails_RadiationDevice_Model',
                   'Depth': 'depth'}
    
    choices = choices_dict.keys()
    #### Traits UI views ######################################################

    trait_view = View(Group(Item('match_traits',editor=SetEditor(name='choices',
                    can_move_all=True, ordered=False, 
                    left_column_title = 'Beam Parameters',
                    right_column_title = 'Parameters to Match'),show_label=False),
                    label='Default Parameters a Reference Beam Must Match'))
                    

#### EOF ######################################################################
