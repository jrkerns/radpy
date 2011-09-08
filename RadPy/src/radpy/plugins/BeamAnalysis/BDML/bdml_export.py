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

from lxml import etree, objectify
from radpy.plugins.BeamAnalysis.view.beam_xml import Beam

def bdml_export(beam_list, filename, progress=None):
    """Accepts a list of beam objects and saves it to filename in BDML format"""
    
    #Is beam_list a list of beam objects or tuples? (Model passes list of 
    #tuples)
    if isinstance(beam_list[0], tuple):
        beam_list = [j for i in beam_list for j in i if isinstance(j, Beam)]
    
    NSMAP = {'xsi' : "http://www.w3.org/2001/XMLSchema-instance"}
    xml_tree = etree.ElementTree(objectify.Element("{http://www.radpy.org}BDML",
                                                   nsmap=NSMAP))
    xml_root = xml_tree.getroot()
    xml_root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation",
                 "http://www.radpy.org/BDML/BDML.xsd")
    
    for value, i in enumerate(beam_list):
        if progress:
            progress.setValue(value)
        temp = etree.SubElement(xml_root,"{http://www.radpy.org}Beam")
        xml_root.Beam[-1] = i.exportXML()
    
    #Get rid of objectify namespace    
    objectify.deannotate(xml_tree)
    etree.cleanup_namespaces(xml_tree)
    
    file = open(filename,'w')
    xml_tree.write(file, pretty_print=True)
    file.close()
