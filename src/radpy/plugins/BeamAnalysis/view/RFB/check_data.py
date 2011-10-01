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

from rfb import *
import csv

def check_data(file):
    f = open(file,'rb')
    a = beam.parse(f.read())
    f.close()
    return a

def load_multi_data(file):
    f = open(file,'rb')
    a = multi_data_file.parse(f.read())
    f.close()
    return a

def testop(file):
    f = open(file,'rb')
    a = test.parse(f.read())
    f.close()
    return a

def beam_dump(infile,outfile):
    f = open(infile,'rb')
    a = test.parse(f.read())
    f.close()

    f = open(outfile,'wb')
    writer = csv.writer(f)
    keys = []
    main_keys = ['rad_device','energy','particle','inline_jaw_negative',
                 'inline_jaw_positive','crossline_jaw_negative',
                 'crossline_jaw_positive','gantry_angle',
                 'wedge_type', 'wedge_angle','SSD','scan_type']
    measurement_keys = ['peff_offset','modified_date','scan_start_crossline',
                        'scan_start_inline','scan_start_depth','scan_end_crossline',
                        'scan_end_inline','scan_end_depth']
    #for i in a[0].main_header.keys():
    #    main_keys.append(i)
    #for i in a[0].measurement_header.keys():
    #    measurement_keys.append(i)
    keys += main_keys
    keys += measurement_keys
    writer.writerow(keys)

    for i in a:
        tmprow = []
        for j in main_keys:
            tmprow.append(i.main_header[j])
        for j in measurement_keys:
            tmprow.append(i.measurement_header[j])

        writer.writerow(tmprow)

    f.close()
    
