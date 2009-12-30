'''
Created on Jul 13, 2009

@author: Stephen_Terry
'''
import os
from os.path import join

import dicom 

class RTPlan(object):
    '''
    classdocs
    '''


    def __init__(self,uid,directory):
        '''
        Constructor
        '''
        filenames = []
        for root,dirs,files in os.walk(directory):
            for f in files:
                if f.endswith('.dcm'):
                    filenames.append(os.path.join(root, f))

        for name in filenames:
            try:
                self.dicom_file = dicom.ReadFile(name)
                if self.dicom_file.SOPInstanceUID == uid and \
                    self.dicom_file.SOPClassUID == 'RT Plan Storage':
                    break 
            except:
                pass
        else:
            self.dicom_file = None
            