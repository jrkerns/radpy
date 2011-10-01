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

import struct
import sys
from numpy import append, array
import datetime

from radpy.plugins.BeamAnalysis.view.construct import *
#from construct import *
#from radpy.plugins.BeamAnalysis.view.beam_traits import Beam


#This is a description file based on Construct 
#(http://construct.wikispaces.com/), a library to simplify parsing
#of binary data.
#
#Usage: 
#    from rfb import omnipro_file
#    a = omnipro_file.parse(*data buffer*)
#
#    omnipro_file.parse will return a list of Beam objects, each with
#    full header data for that particular measurement.
#
#Omnipro rfb file structure: Each scan within an rfb file contains two 
#parts: header and data.  The header is also divided into two parts.
#The first part, what I call the main header, contains information about
#the scan that pertains to linear accelerator parameters (energy,
#field size, particle, gantry angle, etc.)  The second part, what I call
#the measurement header, contains parameters relevant to the Phantom
#(scan start and end positions, scan speed, electrometer voltages, etc.)
#The information in the main header can apply to more than one scan, for
#example 5 profiles at different depths but all with the same
#energy, field size, etc.  Therefore, the rfb file conserves space by
#only including the main header if something changes between scans.

#The basic file format is as follows:  

#Omnipro Version number
#Main header of one group of scans
#Measurement header and data for each scan for one measurement type,
#   (depth dose, profile)
#Measurement header and data for another measurement type, but same main
#   header info.
#Main header of another group of scans
#Measurement header and data for each scan (could be either data type)
#...
#12 \x00 bytes to mark end of file

#For some reason, the headers of the first group of scans and the
#following groups are different.  Thus we need two types of scan
#adapters (and some convoluted switching code) to process the file.
#This is the basic program flow with structure names included:

#Read main_header
#If different measurement type but same main header data, read
#   new_scan_type_header
#If new main header data, read additional_header
#Continue calling additional_header until end of file reached.

#For a better description of the file format look at the beam Struct
#at the end of the file.  It contains a description of the file format
#for an rfb file that contains only a single scan.  It has none of the
#multiple scan weirdness.
    
class ScanTypeAdapter(Adapter):
    
    """Given a sequence of bytes, returns the last byte converted from
    short binary format.  Used to determine if the following header has
    new main header information."""
    
    def _decode(self, obj, context):         
        return struct.unpack('b', obj[-1])[0]
    
class Beam(object):
    """ A holder object with dictionaries of quantities extracted from the 
    .rfb files. """
    
    def __init__(self):
        self.main_header = {}
        self.measurement_header = {}
        self.abscissa = []
        self.ordinate = []
        self.data_elements = {}
            
#    def machine_axes_to_xyz(self, coordinate):
#        """ Given a point in machine coordinates, converts it to xyz """
#        """ Accepts a tuple of coordinates in machine terms (crossplane, inplane,
#        depth) and returns a numpy 1D array of xyz coordinates.  Uses the 
#        servo axis values in the measurement header for the conversion. 
#        
#        The coordinate system used is DICOM standard (IEC 1217).  For a patient
#        in the head first supine position, the Y axis runs inferior to superior,
#        the Z axis runs anterior-posterior and the X axis runs patient right to 
#        patient left."""
#        
#        crossplane = self.get_machine_axis_vector(
#                        self.measurement_header['crossplane_servo_axis'])
#        inplane = self.get_machine_axis_vector(
#                        self.measurement_header['inplane_servo_axis'])
#        depth = self.get_machine_axis_vector(
#                        self.measurement_header['depth_servo_axis'])
#        
#        xyz_vector = coordinate[0]*crossplane + coordinate[1]*inplane + \
#                        coordinate[2]*depth
#                        
#        return xyz_vector
    
    def get_machine_axis_vector(self, value):
        
        vector = array([0,0,0])
        if 'x' in value:
            vector[0] = 1
        elif 'y' in value:
            vector[1] = 1
        elif 'z' in value:
            vector[2] = 1
        
        if 'neg' in value:
            vector *= -1
        
            
        return vector
    
    
    def set_xml_elements(self, data_structure):
        """Takes an XML beam object and populates the BDML tree."""
        #The BDML tree contained in a beam_xml.Beam object is populated with
        #values taken from the dictionaries (self.main_header, 
        #self.measurement_header, etc.) that the Construct parser returns.
        #The coordinate system used is IEC fixed gantry and collimator (as you
        #stand at the couch looking towards the gantry, x is
        #crossplane increasing from left to right, y is inplane increasing
        #towards the gantry and z is depth increasing vertically).  The crossplane
        #and inplane coordinates of the origin correspond to those of the 
        #isocenter and the depth coordinate is the water surface.  See the
        #report of Task Group 11 "Information Transfer from Beam Data
        #Acquisition Systems", Figure 1. 
        #http://www.aapm.org/pubs/reports/OR_01.pdf
        #All distances in the RFB file are stored in mm.  They are converted
        #to cm here.
        
#        isocenter_xyz = self.machine_axes_to_xyz(
#                            (self.measurement_header['isocenter_crossplane'],
#                             self.measurement_header['isocenter_inplane'],
#                             self.measurement_header['isocenter_depth']))

        isocenter_xyz = [self.measurement_header['isocenter_crossplane'],
                         self.measurement_header['isocenter_inplane'],
                         -self.measurement_header['isocenter_depth']]
        
        
        data_structure.beam.MeasurementDetails.Isocenter.x = isocenter_xyz[0]/10.
        data_structure.beam.MeasurementDetails.Isocenter.y = isocenter_xyz[1]/10.         
        data_structure.beam.MeasurementDetails.Isocenter.z = isocenter_xyz[2]/10.
            
        
        
#        data_structure.beam.MeasurementDetails.CoordinateAxes.Inplane = \
#            self.measurement_header['inplane_servo_axis']
#        data_structure.beam.MeasurementDetails.CoordinateAxes.Crossplane = \
#            self.measurement_header['crossplane_servo_axis']
#        data_structure.beam.MeasurementDetails.CoordinateAxes.Depth = \
#            self.measurement_header['depth_servo_axis']
            
        data_structure.beam.MeasurementDetails.MeasuredDateTime = \
            datetime.datetime.fromtimestamp(
                self.measurement_header['measured_date']).isoformat()
            #time.asctime(time.gmtime(self.measurement_header['measured_date']))
            
        
        data_structure.beam.MeasurementDetails.ModificationHistory.Record = \
            datetime.datetime.fromtimestamp(
                self.measurement_header['modified_date']).isoformat() + ',' + \
                self.measurement_header['measurement_comment']
        
        start_pos_xyz = [self.measurement_header['scan_start_crossplane'],
                             self.measurement_header['scan_start_inplane'],
                             self.measurement_header['scan_start_depth']]
        
        data_structure.beam.MeasurementDetails.StartPosition.x = \
            start_pos_xyz[0]/10.# - isocenter_xyz[0]
        data_structure.beam.MeasurementDetails.StartPosition.y = \
            start_pos_xyz[1]/10.# - isocenter_xyz[1]
        data_structure.beam.MeasurementDetails.StartPosition.z = \
            -start_pos_xyz[2]/10.# - isocenter_xyz[2]
        
        
        stop_pos_xyz = [self.measurement_header['scan_end_crossplane'],
                             self.measurement_header['scan_end_inplane'],
                             self.measurement_header['scan_end_depth']]
        
        data_structure.beam.MeasurementDetails.StopPosition.x = \
            stop_pos_xyz[0]/10.# - isocenter_xyz[0]
        data_structure.beam.MeasurementDetails.StopPosition.y = \
            stop_pos_xyz[1]/10.# - isocenter_xyz[1]
        data_structure.beam.MeasurementDetails.StopPosition.z = \
            -stop_pos_xyz[2]/10.# - isocenter_xyz[2]
        
        data_structure.beam.MeasurementDetails.Physicist.EmailAddress = \
            self.main_header['email']
            
        data_structure.beam.MeasurementDetails.Physicist.Telephone = \
            self.main_header['telephone']
            
        data_structure.beam.MeasurementDetails.Physicist.Name = ''
        
        data_structure.beam.MeasurementDetails.Physicist.Institution = \
            self.main_header['institution']
            
        data_structure.beam.MeasurementDetails.Medium = \
            self.main_header['medium']
                    
        data_structure.beam.MeasurementDetails.Servo.Model = \
            self.measurement_header['servo_type']
        data_structure.beam.MeasurementDetails.Servo.Vendor = \
            'IBA Dosimetry'
        
        data_structure.beam.MeasurementDetails.Electrometer.Model = \
            self.measurement_header['electrometer_type']
            
        data_structure.beam.MeasurementDetails.Electrometer.Vendor = \
            'IBA Dosimetry'
            
        data_structure.beam.MeasurementDetails.Electrometer.Voltage = \
            self.measurement_header['field_hv']
        
        data_structure.beam.MeasurementDetails.MeasuringDevice.Model = \
            self.measurement_header['detector']
            
        data_structure.beam.MeasurementDetails.MeasuringDevice.Manufacturer = \
            'IBA Dosimetry'
        
        data_structure.beam.MeasurementDetails.MeasuringDevice.Type = \
            self.measurement_header['detector_type']
        
        data_structure.beam.BeamDetails.Energy = \
            self.main_header['energy']
            
        data_structure.beam.BeamDetails.Particle = \
            self.main_header['particle']
            
        data_structure.beam.BeamDetails.SAD = \
            self.main_header['SAD']/10.
            
        data_structure.beam.BeamDetails.SSD = \
            self.main_header['SSD']/10.
            
        data_structure.beam.BeamDetails.CollimatorAngle= \
            self.main_header['collimator_angle']
            
        data_structure.beam.BeamDetails.GantryAngle= \
            self.main_header['gantry_angle']
        
        data_structure.beam.BeamDetails.CrossplaneJawPositions.NegativeJaw = \
            -self.main_header['crossplane_jaw_negative']/10.
        
        data_structure.beam.BeamDetails.CrossplaneJawPositions.PositiveJaw = \
            self.main_header['crossplane_jaw_positive']/10.
        
        data_structure.beam.BeamDetails.InplaneJawPositions.NegativeJaw = \
            -self.main_header['inplane_jaw_negative']/10.
            
        data_structure.beam.BeamDetails.InplaneJawPositions.PositiveJaw = \
            self.main_header['inplane_jaw_positive']/10.
        
        data_structure.beam.BeamDetails.Wedge.Angle = \
            self.main_header['wedge_angle']
            
        data_structure.beam.BeamDetails.Wedge.Type = \
            self.main_header['wedge_type']
            
        data_structure.beam.BeamDetails.Applicator = \
            self.main_header['applicator']
            
        data_structure.beam.BeamDetails.Accessory = \
            ''
        
        data_structure.beam.BeamDetails.RadiationDevice.Vendor = \
            ''
        data_structure.beam.BeamDetails.RadiationDevice.Model = \
            self.main_header['rad_device']
            
        data_structure.beam.BeamDetails.RadiationDevice.SerialNumber = \
            ''
        
        scale = self.main_header['gantry_scale']
        if scale == 'CW_180_Down':
            data_structure.beam.BeamDetails.RadiationDevice.MachineScale = 'IEC 1217'
        elif scale == 'CW_180_Up':
            data_structure.beam.BeamDetails.RadiationDevice.MachineScale = 'Varian IEC'
        
        #data_structure.quantity = self.measurement_header['data_type']

class DataFileAdapter(Adapter):
    
    """Converts the data read from the rfb file format to a list of Beam
    objects each with full header information"""
    
    def _decode(self, obj, context):
        beams = []
        
        for i in range(obj.main_header.num_scans_with_this_header):
            try:
                beam_tmp = Beam()
                for j in obj.main_header.__dict__.keys():
                    if j != "measurement_data":
                        beam_tmp.main_header[j] = obj.main_header[j]
                for j in obj.main_header.measurement_data[i].__dict__.\
                                keys():
                    if j != "data":
                        beam_tmp.measurement_header[j] = \
                            obj.main_header.measurement_data[i][j]
                for j in obj.main_header.measurement_data[i].data.data:
#                    beam_tmp.data_abscissa.append(j[0])
#                    beam_tmp.data_ordinate.append(j[1])
                    beam_tmp.abscissa = append(beam_tmp.abscissa,j[0])
                    beam_tmp.ordinate = append(beam_tmp.ordinate,j[1])
                beams.append(beam_tmp)
            except:
                print sys.exc_info()[0]
                raise

        if obj.first_sub_header != None and \
            obj.first_sub_header.measurement_data != None:
            if obj.first_sub_header.__dict__.has_key("energy") == False:
                
                for i in range(len(
                    obj.first_sub_header.measurement_data)):
                    try:
                        beam_tmp = Beam()
                        for j in obj.main_header.__dict__.keys():
                            if j != "measurement_data":
                                beam_tmp.main_header[j] = \
                                    obj.main_header[j]
                        for j in obj.first_sub_header.\
                            measurement_data[i].__dict__.keys():
                            if j != "data":
                                beam_tmp.measurement_header[j] = \
                                    obj.first_sub_header.\
                                        measurement_data[i][j]
                        for j in obj.first_sub_header.\
                                measurement_data[i].data.data:
        #                    beam_tmp.data_abscissa.append(j[0])
        #                    beam_tmp.data_ordinate.append(j[1])
                            beam_tmp.abscissa = append(beam_tmp.abscissa,j[0])
                            beam_tmp.ordinate = append(beam_tmp.ordinate,j[1])
                        
                        beams.append(beam_tmp)
                    except:
                        pass
                    
            else:
                
                for j in range(len(
                    obj.first_sub_header.measurement_data)):
                    try:
                        beam_tmp = Beam()
                        for k in obj.first_sub_header.__dict__.keys():
                            if k != "measurement_data" and \
                                   k != "scan_type":
                                beam_tmp.main_header[k] = \
                                    obj.first_sub_header[k]
                        for k in obj.first_sub_header.\
                                measurement_data[j].__dict__.keys():
                            if k != "data":
                                beam_tmp.measurement_header[k] = \
                                    obj.first_sub_header.\
                                        measurement_data[j][k]
                                                   
                        for k in obj.first_sub_header.\
                                measurement_data[j].data.data:
#                            beam_tmp.data_abscissa.append(k[0])
#                            beam_tmp.data_ordinate.append(k[1])
                            beam_tmp.abscissa = append(beam_tmp.abscissa,k[0])
                            beam_tmp.ordinate = append(beam_tmp.ordinate,k[1])

                        beams.append(beam_tmp)
                    except:
                        pass

            for i in range(len(obj.add_header)):
                try:
                    for j in range(len(obj.add_header[i].\
                                       measurement_data)):
                        try:
                            beam_tmp = Beam()
                            for k in obj.add_header[i].__dict__.keys():
                                if k != "measurement_data" and k != \
                                       "scan_type":
                                    beam_tmp.main_header[k] = \
                                        obj.add_header[i][k]
                            for k in obj.add_header[i].\
                                    measurement_data[j].__dict__.keys():
                                if k != "data":
                                    beam_tmp.measurement_header[k] = \
                                        obj.add_header[i].\
                                            measurement_data[j][k]
                                
                            for k in obj.add_header[i].\
                                    measurement_data[j].data.data:
#                                beam_tmp.data_abscissa.append(k[0])
#                                beam_tmp.data_ordinate.append(k[1])
                                beam_tmp.abscissa = append(beam_tmp.abscissa,k[0])
                                beam_tmp.ordinate = append(beam_tmp.ordinate,k[1])

                            beams.append(beam_tmp)
                        except:
                            pass
                except:
                    pass

        return beams


measurement_data = Struct("measurement_data",
    
    SNInt32("measured_date"),
    SNInt32("modified_date"),
    
    Enum(UNInt8("data_type"),
         relative_optical_density = 1,
         relative_dose = 2,
         relative_ionization = 3,
         absolute_dose = 4,
         charge = 5,
         _default_ = "unknown"
    ),
    NFloat64("chamber_radius"),
    NFloat64("calibration_factor"),
    
    NFloat64("unknown1"),
    NFloat64("unknown2"),
    
    PascalString("calibration_date"),
    
    NFloat64("peff_offset"),
    PascalString("detector"),
    Enum(UNInt8("detector_type"),
         single_diode = 1,
         LDA11 = 2,
         LDA25 = 3,
         ion_chamber_cylinder = 4,
         ion_chamber_parallel = 5,
         stereotactic = 6,
         film = 7,
         CA24 = 8,
         BIS_2G = 9,
         BIS_710 = 10,
         LDA99 = 11,
         _default_ = "unknown"
    ),
    Field("raw2",1),                      
    
    PascalString("operator"),
    PascalString("measurement_comment"),
    Enum(SNInt16("crossplane_servo_axis"),
         z_neg = -3,
         y_neg = -2,
         x_neg = -1,
         x_pos = 1,
         y_pos = 2,
         z_pos = 3,
         _default_ = "unknown"
         
    ),
    Enum(SNInt16("inplane_servo_axis"),
         z_neg = -3,
         y_neg = -2,
         x_neg = -1,
         x_pos = 1,
         y_pos = 2,
         z_pos = 3,
         _default_ = "unknown"
    ),
    Enum(SNInt16("depth_servo_axis"),
         z_neg = -3,
         y_neg = -2,
         x_neg = -1,
         x_pos = 1,
         y_pos = 2,
         z_pos = 3,
         _default_ = "unknown"
    ),
    UNInt16("measurements_per_point"),
    Field("raw3",2),
    
    NFloat64("scan_speed"),
                       
    
    Enum(UNInt16("servo_type"),
         HSCAN1 = 1,
         HSCAN2 = 2,
         table_scanner = 3,
         blue_2d = 4,
         Acryl_48_48_48 = 5,
         Acryl_48_48_29 = 6,
         Acryl_48_29_29 = 7,
         Acryl_48_13_29 = 8,
         Acryl_29_29_29 = 9,
         blue_1st_48_48_48 = 10,
         blue_1st_48_48_41 = 11,
         blue_48_48_48 = 12,
         blue_48_48_41 = 13,
         air_1d = 14,
         air_2d_fdm300 = 15,
         air_2d_rfa200 = 16,
         air_mounted_2d = 17,
         rfa200 = 18,
         rfa_50_50_50 = 19,
         rfa_50_50_40 = 20,
         rfa_40_40_40 = 21,
         fdm = 22,
         fdm_200 = 23,
         fdm_300 = 24,
         vxr12 = 25,
         dosim_pro = 26,
         lumisys = 27,
         wp102_densitometer = 28,
         _default_ = "unknown"
    ),                
    Enum(UNInt16("measurement_mode_a"),
         dose_mode = 1,
         beam_on_off = 2,
         absolute = 3,
         absolute_dosimetry = 4,
         dose_rate = 5,
         continuous = 6,
         scanned = 7,
         step_by_step = 8,
         _default_ = "unknown"
    ),
    Field("raw4_b",6),
    NFloat64("isocenter_crossplane"),
    NFloat64("isocenter_inplane"),
    NFloat64("isocenter_depth"),
    NFloat64("normalization_crossplane"),
    NFloat64("normalization_inplane"),
    NFloat64("normalization_depth"),
    
    
    NFloat64("field_normalization"),
    NFloat64("reference_normalization"),
    NFloat64("field_dark_current"),
    NFloat64("reference_dark_current"),
    NFloat64("field_hv"),
    NFloat64("reference_hv"),
    SNInt16("field_gain"),
    SNInt16("reference_gain"),
    PascalString("field_range"),
    PascalString("reference_range"),
    NFloat64("water_surface_correction"),
    Enum(Byte("measurement_mode_b"),
        field_channel = 1,
        reference_division = 2,
        _default_ = "none"
    ),
    Field("raw5",1),
    
       
    Enum(Byte("HV_connection"),
        floated = 1,
        grounded = 2,
        _default_ = "none"
    ),
    
    Field("raw6",1),
    NFloat64("reference_maximum"),
    NFloat64("reference_minimum"),
    NFloat64("reference_average"),
    NFloat64("electrometer_sampling_time"),
    Enum(SNInt16("electrometer_type"),
         DPD_510 = 1,
         emX = 2,
         CU500 = 3,
         CU500E = 4,
         MCU = 5,
         MD240 = 6,
         WP5006 = 7,
         WP5007 = 8,
         emXX = 9,
         CCU = 10,
        
        _default_ = "none"
    ),
    
    NFloat64("renormalization_factor"),
    NFloat64("curve_offset"),
    
    
    PascalString("setup_comment"),
    Flag("ca24_calibration"),
    
           
    Padding(1),
    NFloat64("position_a_crossplane"),
    NFloat64("position_a_inplane"),
    NFloat64("position_a_depth"),
    NFloat64("position_b_crossplane"),
    NFloat64("position_b_inplane"),
    NFloat64("position_b_depth"),
    NFloat64("position_c_crossplane"),
    NFloat64("position_c_inplane"),
    NFloat64("position_c_depth"),
    NFloat64("position_d_crossplane"),
    NFloat64("position_d_inplane"),
    NFloat64("position_d_depth"),
    Field("raw9",10),
    
    NFloat64("scan_start_crossplane"),
    NFloat64("scan_start_inplane"),
    NFloat64("scan_start_depth"),
    NFloat64("scan_end_crossplane"),
    NFloat64("scan_end_inplane"),
    NFloat64("scan_end_depth"),
    
    #Next two bytes are number of data points in this scan.
    Struct("data",
           SNInt16("length"),
           #Read in pairs (abscissa/ordinate) of 8 byte floats 
           #until the number reaches the number of data points.
           MetaRepeater(lambda ctx: ctx["length"],
                        StrictRepeater(2,NFloat64("data"))),
    ),
    
    
)

main_measurement_data = Struct("measurement_data",
    Embed(measurement_data),
    Padding(2)
)


#Additional measurements are separated by certain delimiters.   If
#the next scan uses the same main header, then the delimiter is only
#two bytes long and ends in '\x80'.  If the next scan changes 
#information in the main header, then the delimiter is more than two
#bytes long.  Therefore, additional_measurement_data checks to see if the 
#next three bytes beyond the '\x80' marker are zero.  If so, it exits back
#to the additional_header Struct.  If not, it reads in another
#measurement_data section.
 
additional_measurement_data = RepeatUntil(lambda obj, ctx: \
    obj["delimiter"] != 128 and obj["delimiter2"] == 0,
    Struct("measurement_data",
        
        Embed(measurement_data),
        
        Padding(1),
        Byte("delimiter"),
        Peek(ScanTypeAdapter(Field("delimiter2",3))),
        
            
        If(lambda ctx: ctx["delimiter"] == 0 and ctx["delimiter2"] != 0,
            RepeatUntil(lambda obj, ctx: \
                        obj == "\x80", Field("raw", 1))),
        
    )
)

        
new_scan_type_header = Struct("new_scan_type_header",
   
    Padding(5),
    Embed(Struct("scan_type_field",
    Byte("length"),
    Padding(2),
    MetaField("scan_type", lambda ctx: ctx["length"]-1)
        )
    ),
    
    MetaRepeater(lambda ctx: ctx["_"]["num_scans_with_this_header"],
                 main_measurement_data)
)


header_data = Struct("header_data",
    #Something about CBeam in the following padding.  Differentiate data types?
    Padding(13),
    PascalString("rad_device"),
    Padding(2),
    NFloat64("energy"),
    Enum(UNInt8("particle"),
         Photon = 0,
         Electron = 1,
         Proton = 2,
         Neutron = 3,
         Cobalt = 4,
         Isotope = 5,
         _default_ = "unknown"
    ),
    Padding(1),
    Enum(SNInt16("wedge_type"),
         Open = -1,
         Hard_Wedge = 0,
         Dynamic_Wedge = 1,
         Enhanced_Wedge = 2,
         Virtual_Wedge = 3,
         Soft_Wedge = 4,
         _default_ = "unknown"
    ),
    Padding(2),
    UNInt8("wedge_angle"),
    Padding(3),
    UNInt16("gantry_angle"),
    Padding(2),
    UNInt16("collimator_angle"),
    Padding(2),
    NFloat64("SSD"),
    Padding(2),
    NFloat64("SAD"),
    PascalString("applicator"),
    Enum(SNInt8("medium"),
         Air = 0,
         Water = 1,
         Film = 2,
         _default_ = "unknown"
    ),
    Padding(1),
    PascalString("institution"),
    PascalString("address"),
    PascalString("telephone"),
    PascalString("email"),
    Padding(2),
    NFloat64("inplane_jaw_negative"),
    Padding(2),
    NFloat64("inplane_jaw_positive"),
    Padding(2),
    NFloat64("crossplane_jaw_negative"),
    Padding(2),
    NFloat64("crossplane_jaw_positive"),
    Enum(UNInt8("gantry_scale"),
         CW_180_Down = 0,
         CCW_180_Down = 1,
         CW_180_Up = 2,
         CCW_180_Up = 3,
         _default_ = "unknown"
    ),
    Padding(1),              

    #Different curve types have different numbers of \x00 repeated
    #before giving the curve type.  This RepeatUntil iterates until 
    #a byte different than \x01 is reached.
                     
    ScanTypeAdapter(RepeatUntil(lambda obj, ctx: obj != "\x00", Field(
        "num_scans_with_this_header",1))),
    Padding(5),
    Embed(Struct("scan_type_field",
           Byte("length"),
           Padding(2),
           MetaField("scan_type", lambda ctx: ctx["length"]-1)
           )
    )
)

main_header = Struct("main_header",
    PascalString("omnipro_version"),
    Embed(header_data),
    
    MetaRepeater(lambda ctx: ctx["num_scans_with_this_header"],
                 main_measurement_data)
)
    
#Additional header sections are delimited by a sequence of \x00 values
#and then by \x80.  This header is similar to the main header, but
#does not contain a scan type (depth dose/profile) field.

additional_header = Struct("add_header",
    RepeatUntil(lambda obj, ctx: obj == "\x80", Field("raw", 1)),
    PascalString("rad_device"),
    Padding(2),
    NFloat64("energy"),
     
    Enum(UNInt8("particle"),
         Photon = 0,
         Electron = 1,
         Proton = 2,
         Neutron = 3,
         Cobalt = 4,
         Isotope = 5,
         _default_ = "unknown"
    ),
    UNInt8("raw"),
    
    Enum(SNInt16("wedge_type"),
         Open = -1,
         Hard_Wedge = 0,
         Dynamic_Wedge = 1,
         Enhanced_Wedge = 2,
         Virtual_Wedge = 3,
         Soft_Wedge = 4,
         _default_ = "unknown"
    ),
    Padding(2),
    UNInt8("wedge_angle"),
    Padding(3),
    UNInt16("gantry_angle"),
    Padding(2),
    UNInt16("collimator_angle"),
    Padding(2),
    NFloat64("SSD"),
    Padding(2),
    NFloat64("SAD"),
    PascalString("applicator"),
    
    Enum(SNInt8("medium"),
         Air = 0,
         Water = 1,
         Film = 2,
         _default_ = "unknown"
    ),
    Padding(1),
    
    PascalString("institution"),
    PascalString("address"),
    PascalString("telephone"),
    PascalString("email"),
    Padding(2),
    NFloat64("inplane_jaw_negative"),
    Padding(2),
    NFloat64("inplane_jaw_positive"),
    Padding(2),
    NFloat64("crossplane_jaw_negative"),
    Padding(2),
    NFloat64("crossplane_jaw_positive"),
    
    Enum(UNInt8("gantry_scale"),
         CW_180_Down = 0,
         CCW_180_Down = 1,
         CW_180_Up = 2,
         CCW_180_Up = 3,
         _default_ = "unknown"
    ),
    Padding(1),
    
    Enum(Byte("scan_type"),
         DepthDose = 0,
         _default_ = "Profile"),
    
    
    RepeatUntil(lambda obj, ctx: obj == "\x80", Field("raw", 1)),
    
    Optional(additional_measurement_data)
)
            
#This is the main Struct to read in a RFB file with multiple scans.
#Logic:
#Read main_header
#If the next scan is a different measurement type but the 
#    same main header data, read new_scan_type_header
#If the scan has different main header data, read additional_header
#Continue calling additional_header until end of file reached.

multi_data_file = Struct("opfile",
    main_header,
    
    ScanTypeAdapter(Field("num_scans_with_this_header",3)),
    
    
    Optional(Switch("first_sub_header",lambda ctx: \
                    ctx["num_scans_with_this_header"],
    {0 : additional_header},
    default = new_scan_type_header)
    ),
    
    OptionalGreedyRepeater(additional_header),
    
)

omnipro_file = DataFileAdapter(multi_data_file)


### Beam Struct is not used, but is in this file as documentation of 
### omnipro rfb file data format.  This would be the structure of a
### data file containing a single beam.

beam = Struct("beam",
    PascalString("omnipro_version"),
    Repeater(13,UNInt8("raw")),
    PascalString("rad_device"),
    Repeater(2,UNInt8("raw")),
    NFloat64("energy"),
    Enum(UNInt8("particle"),
         Photon = 0,
         Electron = 1,
         Proton = 2,
         Neutron = 3,
         Cobalt = 4,
         Isotope = 5,
         _default_ = "unknown"),
    UNInt8("raw"),
    Enum(SNInt16("wedge_type"),
         Open = -1,
         Hard_Wedge = 0,
         Dynamic_Wedge = 1,
         Enhanced_Wedge = 2,
         Virtual_Wedge = 3,
         Soft_Wedge = 4,
         _default_ = "unknown"),
    Repeater(2,UNInt8("raw")),
    UNInt8("wedge_angle"),
    Repeater(3,UNInt8("raw")),
    UNInt16("gantry_angle"),
    Repeater(2,UNInt8("raw")),
    UNInt16("collimator_angle"),
    Repeater(2,UNInt8("raw")),
    NFloat64("SSD"),
    Repeater(2,UNInt8("raw")),
    NFloat64("SAD"),
    PascalString("applicator"),
    Enum(SNInt8("medium"),
         Air = 0,
         Water = 1,
         Film = 2,
         _default_ = "unknown"),
    UNInt8("raw"),
    PascalString("institution"),
    PascalString("address"),
    PascalString("telephone"),
    PascalString("email"),
    Repeater(2,UNInt8("raw")),
    NFloat64("inplane_jaw_negative"),
    Repeater(2,UNInt8("raw")),
    NFloat64("inplane_jaw_positive"),
    Repeater(2,UNInt8("raw")),
    NFloat64("crossplane_jaw_negative"),
    Repeater(2,UNInt8("raw")),
    NFloat64("crossplane_jaw_positive"),
    Enum(UNInt8("gantry_scale"),
         CW_180_Down = 0,
         CCW_180_Down = 1,
         CW_180_Up = 2,
         CCW_180_Up = 3,
         _default_ = "unknown"),
    UNInt8("raw"),              

    #Different curve types have different numbers of \x00 repeated
    #before giving the curve type.  This RepeatUntil iterates until 
    #a byte different than \x01 is reached.
              
    RepeatUntil(lambda obj, ctx: obj == "\x01", Byte(
        "num_scans_with_this_header")),
    Repeater(5,UNInt8("raw")),
    Struct("scan_type",
           Byte("length"),
           Byte("raw"),
           Byte("raw"),
           MetaField("scan", lambda ctx: ctx["length"]-1)
           ),

    #Dates are given in epoch time.  Convert to a python struct_time by
    #using gmtime().
    SNInt32("measured_date"),
    SNInt32("modified_date"),
    
    Enum(UNInt8("data_type"),
         relative_optical_density = 1,
         relative_dose = 2,
         relative_ionization = 3,
         absolute_dose = 4,
         charge = 5,
         _default_ = "unknown"),
    NFloat64("chamber_radius"),
    NFloat64("calibration_factor"),
    Repeater(17,UNInt8("raw")),
    NFloat64("peff_offset"),
    PascalString("detector"),
    Enum(UNInt8("detector_type"),
         single_diode = 1,
         LDA11 = 2,
         LDA25 = 3,
         ion_chamber_cylinder = 4,
         ion_chamber_parallel = 5,
         stereotactic = 6,
         film = 7,
         CA24 = 8,
         BIS_2G = 9,
         BIS_710 = 10,
         LDA99 = 11,
         _default_ = "unknown"),
    UNInt8("raw"),
    PascalString("operator"),
    PascalString("measurement_comment"),
    Repeater(10,UNInt8("raw")),
    NFloat64("scan_speed"),
    Repeater(58,UNInt8("raw")),
    NFloat64("field_normalization"),
    NFloat64("reference_normalization"),
    NFloat64("field_dark_current"),
    NFloat64("reference_dark_current"),
    NFloat64("field_hv"),
    NFloat64("reference_hv"),
    SNInt16("field_gain"),
    SNInt16("reference_gain"),
    PascalString("field_range"),
    PascalString("reference_range"),
    NFloat64("water_surface_correction"),
    Repeater(4,UNInt8("raw")),
    NFloat64("reference_maximum"),
    NFloat64("reference_minimum"),
    NFloat64("reference_average"),
    Repeater(26,UNInt8("raw")),
    PascalString("setup_comment"),
    Flag("ca24_calibration"),
    UNInt8("raw"),
    NFloat64("position_a_crossplane"),
    NFloat64("position_a_inplane"),
    NFloat64("position_a_depth"),
    NFloat64("position_b_crossplane"),
    NFloat64("position_b_inplane"),
    NFloat64("position_b_depth"),
    NFloat64("position_c_crossplane"),
    NFloat64("position_c_inplane"),
    NFloat64("position_c_depth"),
    NFloat64("position_d_crossplane"),
    NFloat64("position_d_inplane"),
    NFloat64("position_d_depth"),
    Repeater(10,UNInt8("raw")),
    NFloat64("scan_start_crossplane"),
    NFloat64("scan_start_inplane"),
    NFloat64("scan_start_depth"),
    NFloat64("scan_end_crossplane"),
    NFloat64("scan_end_inplane"),
    NFloat64("scan_end_depth"),
    Struct("data",
           SNInt16("length"),
           MetaRepeater(lambda ctx: ctx["length"],
                        StrictRepeater(2,NFloat64("data")))
           )
         
                            )

