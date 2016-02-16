# RadPy #

RadPy is a project to simplify analysis of data used in medical physics with an emphasis on radiation therapy. The project is open source and all code will be released under either the GNU General Public License v3 or the GNU Lesser General Public License. As of right now, there are two design goals for RadPy.

1. The creation of a standard format for the storage of data where none currently exists. The main impetus for this goal is the proliferation of formats for the storage of scanning profiles of radiation therapy beams. Right now it is very difficult to compare profiles between systems from different vendors. RadPy will hopefully act as a bridge between systems for profile and other data.

2. A tool for the visualization and analysis of data. Ultimately the goal is for RadPy to not only analyze beam profile data but any data written in a readable format (e.g. DICOM). This could include tasks such as IMRT QA, 3D image registration, etc.