# Major package imports.
from setuptools import setup, find_packages

setup(
    name                 = 'radpy.BeamAnalysis',
    version              = '0.0.2',
    author               = 'Radpy',
    author_email         = 'http://code.google.com/p/radpy/',
    license              = 'GPL',
    zip_safe             = False,
    packages             = find_packages(),
    include_package_data = True,
    
    
    namespace_packages = ['radpy','radpy.BeamAnalysis'],
    
    entry_points         = """
    [enthought.envisage.plugins]
    radpy.BeamAnalysis = \
    radpy.BeamAnalysis.BeamAnalysis_workbench_plugin:BeamAnalysisWorkbenchPlugin
    """
)
