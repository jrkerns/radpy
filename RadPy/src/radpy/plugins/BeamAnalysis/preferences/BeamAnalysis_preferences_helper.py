# -*- coding:utf-8 -*-
"""
Created on Feb 18, 2011

@author: terrst1
"""

from enthought.preferences.api import PreferencesHelper, Preferences
from enthought.traits.api import List
from enthought.etsconfig.api import ETSConfig
from os.path import join

filename = join(ETSConfig.get_application_data(create=False),'radpy','preferences.ini')
PreferencesHelper.preferences = Preferences(filename=filename)

class BeamAnalysisPreferencesHelper(PreferencesHelper):
    """ A preferences helper for the BeamAnalysis plugin. """

    preferences_path = 'radpy.plugins.BeamAnalysis'
    match_traits = List
    