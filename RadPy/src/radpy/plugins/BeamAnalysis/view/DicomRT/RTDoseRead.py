'''
Created on Jul 13, 2009

@author: Stephen_Terry
'''
import struct
import os

import dicom
import numpy
from scipy import ndimage
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from RTPlanRead import RTPlan


class RTDose(object):
    '''
    This class accepts a filename of a DICOM RT Dose object, then reads the
    corresponding RT Plan file.  It then generates a 3D numpy array with
    the units given from the RT Dose file (usually Gy).
    
    The coordinate system used is DICOM standard (IEC 1217).  For a patient
    in the head first supine position, the Z axis runs inferior to superior,
    the Y axis runs anterior-posterior and the X axis runs patient right to 
    patient left.  The class uses the RT Plan isocenter position as the 
    origin of this coordinate system.
    
    To be used in RadPy, the coordinate system should correspond to the IEC
    standard gantry and collimator fixed system where x is the crossplane 
    direction, y is the inplane direction and z is depth.
    '''


    def __init__(self,filename):
        '''
        filename is a string containing the full path to a DICOM RT Dose file.
        '''
        tmp = dicom.read_file(filename)
        self.dose_unit = tmp.DoseUnits
        
        #Call the RTPlan module to find RT Plan DICOM file with same
        #SOP Instance UID
        self.plan = RTPlan(tmp[0x300c,0x0002][0].ReferencedSOPInstanceUID
                           ,os.path.dirname(filename))
        if len(self.plan.dicom_file[0x300a,0x00b0].value) > 1:
            raise IOError('Plans with multiple fields are not supported.')
        self.beam = self.plan.dicom_file[0x300a,0x00b0][0]
        self.machine = self.beam.TreatmentMachineName
        self.SAD = self.beam[0x300a,0x00b4]
        self.particle = self.beam.RadiationType
        self.field = self.beam[0x300a,0x0111][0]
        self.energy = self.field.NominalBeamEnergy
        
        try:
            self.wedge_type = self.beam.Wedges[0].WedgeType
            self.wedge_angle = self.beam.Wedges[0].WedgeAngle
        except:
            pass
        self.meas_manu = self.plan.dicom_file.Manufacturer
        self.meas_model = self.plan.dicom_file.ManufacturersModelName
        self.rad_vend = self.beam.Manufacturer
        self.rad_model = self.beam.ManufacturersModelName
        self.rad_serial = self.beam.DeviceSerialNumber
        self.coll_x_neg = self.field[0x300a,0x011a][0][0x300a,0x011c][0]
        self.coll_x_pos = self.field[0x300a,0x011a][0][0x300a,0x011c][1]
        self.coll_y_neg = self.field[0x300a,0x011a][1][0x300a,0x011c][0]
        self.coll_y_pos = self.field[0x300a,0x011a][1][0x300a,0x011c][1]
        self.gantry_angle = self.field.GantryAngle
        self.collimator_angle = self.field.BeamLimitingDeviceAngle
        self.isocenter = self.field.IsocenterPosition
        if self.gantry_angle != 0 or self.collimator_angle != 0:
            raise IOError('Gantry and collimator angles must be 0 ' + \
                '(IEC Scale).  Instead the plan has a gantry angle of ' + \
                str(self.gantry_angle) + ' and a collimator angle of ' + \
                str(self.collimator_angle) + '.')
        #self.depth_direction = [0,1,0]
        #self.crossplane_direction = [1,0,0]
        #self.inplane_direction = [0,0,1]
        
        
        self.rows = tmp.Rows
        self.columns = tmp.Columns
        self.pixel_spacing = tmp.PixelSpacing
        self.origin = tmp.ImagePositionPatient
        
        #Set up coordinate axes relative to the isocenter
#        self.x_axis_dicom = numpy.arange(self.columns)*self.pixel_spacing[0] + \
#            self.origin[0] - self.isocenter[0]
#        self.y_axis_dicom = numpy.arange(self.rows)*self.pixel_spacing[1] + \
#            self.origin[1] - self.isocenter[1]
#        self.z_axis_dicom = numpy.array(tmp.GridFrameOffsetVector) + \
#            self.origin[2] - self.isocenter[2]
#            
#        #Change DICOM coordinate system to IEC-61217 coordinate system
#        
##        self.x_axis = self.x_axis_dicom
##        self.y_axis = self.z_axis_dicom
##        self.z_axis = -self.y_axis_dicom[::-1]
#        self.x_axis = self.x_axis_dicom
#        self.y_axis = self.y_axis_dicom
#        self.z_axis = self.z_axis_dicom
        self.x_axis = numpy.arange(self.columns)*self.pixel_spacing[0] + self.origin[0]
        self.y_axis = numpy.arange(self.rows)*self.pixel_spacing[1] + self.origin[1]
        self.z_axis = numpy.array(tmp.GridFrameOffsetVector) + self.origin[2]
            
 
        self.dose = numpy.swapaxes(tmp.pixel_array*tmp.DoseGridScaling,0,2)
        a = tmp.pixel_array        
        return
            
        
        
    def get_dose_value(self,x,y,z):
        
        x_coord = (x - self.x_axis[0])/self.pixel_spacing[0]
        
        y_coord = (y - self.y_axis[0])/self.pixel_spacing[1]
        z_coord = (z - self.z_axis[0])/(self.z_axis[1] - self.z_axis[0])
        
        coords = numpy.array([[x_coord],[y_coord],[z_coord]])
        return ndimage.map_coordinates(self.dose, coords, order=1)[0]
        
    
    def get_dose_profile(self,depth=50,direction='depth'):
        
        
        #spacing = numpy.array([self.pixel_spacing[0],self.y_spacing,
        #                      self.pixel_spacing[1]])
        
        if direction == 'depth':
            #depth = self.frame_offset
            #coords = []
            x = numpy.ones(len(self.y_axis))*self.isocenter[0]
            y = self.y_axis
            z = numpy.ones(len(self.y_axis))*self.isocenter[2]
        
        elif direction == 'crossplane':
            
            x = self.x_axis
            y = numpy.ones(len(self.x_axis))*depth
            z = numpy.ones(len(self.x_axis))*self.isocenter[2]
            
        elif direction == 'inplane':
        
            x = numpy.ones(len(self.z_axis))*self.isocenter[0]            
            y = numpy.ones(len(self.z_axis))*depth
            z = self.z_axis
            
        return self.get_dose_value(x,y,z)
            
            
        
    
    def rotate(self,path,gantry,coll,couch):
        
        gantry_matrix = numpy.matrix([[numpy.cos(gantry),numpy.sin(gantry),0],
                                  [numpy.sin(gantry),numpy.cos(gantry),0],
                                  [0,0,1]])
        
        coll_matrix = numpy.matrix([[numpy.cos(coll),0,numpy.sin(coll)],
                                   [0,1,0],
                                  [numpy.sin(coll),0,numpy.cos(coll)]])
        
        couch_matrix = numpy.matrix([[numpy.cos(couch),0,numpy.sin(couch)],
                                   [0,1,0],
                                  [numpy.sin(couch),0,numpy.cos(couch)]])
        
        return gantry_matrix*coll_matrix*couch_matrix*path
        