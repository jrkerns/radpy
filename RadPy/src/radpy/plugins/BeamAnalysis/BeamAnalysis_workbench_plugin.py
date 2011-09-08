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
from enthought.envisage.api import Plugin
from enthought.traits.api import List
from enthought.pyface.workbench.api import TraitsUIView


class BeamAnalysisWorkbenchPlugin(Plugin):
    """ The BeamAnalysis RadPy plugin.
    """

    # Extension points Ids.
    ACTION_SETS       = 'enthought.envisage.ui.workbench.action_sets'
    PERSPECTIVES      = 'enthought.envisage.ui.workbench.perspectives'
    PREFERENCES_PAGES = 'enthought.envisage.ui.workbench.preferences_pages'
    VIEWS             = 'enthought.envisage.ui.workbench.views'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'radpy.plugins.BeamAnalysis'

    # The plugin's name (suitable for displaying to the user).
    name = 'Beam Analysis'

    #### Contributions to extension points made by this plugin ################

    # Action sets.
    action_sets = List(contributes_to=ACTION_SETS)

    def _action_sets_default(self):
        """ Trait initializer. """

        from radpy.plugins.BeamAnalysis.api \
            import BeamAnalysisActionSet
            
        from radpy.plugins.BeamAnalysis.api \
            import BeamAnalysisActionSetUser
         
        return [BeamAnalysisActionSet, BeamAnalysisActionSetUser]

    # Perspectives.
    perspectives = List(contributes_to=PERSPECTIVES)

    def _perspectives_default(self):
        """ Trait initializer. """

        from radpy.plugins.BeamAnalysis.api import BeamAnalysisPerspective

        return [BeamAnalysisPerspective]

    # Preferences pages.
    preferences_pages = List(contributes_to=PREFERENCES_PAGES)

    def _preferences_pages_default(self):
        """ Trait initializer. """

        from radpy.plugins.BeamAnalysis.preferences.api \
            import BeamAnalysisPreferencesPage
        
        return [BeamAnalysisPreferencesPage]

    # Views.
    views = List(contributes_to=VIEWS)

    def _views_default(self):
        """ Trait initializer. """

        from radpy.plugins.BeamAnalysis.api import TreeView
        from radpy.plugins.BeamAnalysis.api import ParameterView

        #return [TreeView, self._create_parameter_view]
        return [TreeView, ParameterView]
    
#    def _create_parameter_view(self, **traits):
#        """ Factory method for the data view. """
#
#        from radpy.plugins.BeamAnalysis.api import ParameterPanel
#
#        parameter_view = TraitsUIView(
#            id   = 'ParameterPanel',
#            name = 'Parameters',
#            obj  = ParameterPanel(),
#            **traits
#        )
#        
#        return parameter_view

#### EOF ######################################################################
