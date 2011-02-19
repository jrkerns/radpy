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

        return [TreeView, self._create_parameter_view]
    
    def _create_parameter_view(self, **traits):
        """ Factory method for the data view. """

        from radpy.plugins.BeamAnalysis.api import ParameterPanel

        parameter_view = TraitsUIView(
            id   = 'ParameterPanel',
            name = 'Parameters',
            obj  = ParameterPanel(),
            **traits
        )
        
        return parameter_view

#### EOF ######################################################################
