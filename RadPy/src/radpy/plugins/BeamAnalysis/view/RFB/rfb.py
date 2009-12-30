import struct
import sys
from numpy import append

from radpy.plugins.BeamAnalysis.view.construct import *

from radpy.plugins.BeamAnalysis.view.beam_traits import Beam


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
                    beam_tmp.data_abscissa = append(beam_tmp.data_abscissa,j[0])
                    beam_tmp.data_ordinate = append(beam_tmp.data_ordinate,j[1])
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
                            beam_tmp.data_abscissa = append(beam_tmp.data_abscissa,j[0])
                            beam_tmp.data_ordinate = append(beam_tmp.data_ordinate,j[1])
                        
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
                            beam_tmp.data_abscissa = append(beam_tmp.data_abscissa,k[0])
                            beam_tmp.data_ordinate = append(beam_tmp.data_ordinate,k[1])

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
                                beam_tmp.data_abscissa = append(beam_tmp.data_abscissa,k[0])
                                beam_tmp.data_ordinate = append(beam_tmp.data_ordinate,k[1])

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
    Enum(SNInt16("crossline_servo_axis"),
         z_neg = -3,
         y_neg = -2,
         x_neg = -1,
         x_pos = 1,
         y_pos = 2,
         z_pos = 3,
         _default_ = "unknown"
         
    ),
    Enum(SNInt16("inline_servo_axis"),
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
    NFloat64("isocenter_crossline"),
    NFloat64("isocenter_inline"),
    NFloat64("isocenter_depth"),
    NFloat64("normalization_crossline"),
    NFloat64("normalization_inline"),
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
    NFloat64("position_a_crossline"),
    NFloat64("position_a_inline"),
    NFloat64("position_a_depth"),
    NFloat64("position_b_crossline"),
    NFloat64("position_b_inline"),
    NFloat64("position_b_depth"),
    NFloat64("position_c_crossline"),
    NFloat64("position_c_inline"),
    NFloat64("position_c_depth"),
    NFloat64("position_d_crossline"),
    NFloat64("position_d_inline"),
    NFloat64("position_d_depth"),
    Field("raw9",10),
    
    NFloat64("scan_start_crossline"),
    NFloat64("scan_start_inline"),
    NFloat64("scan_start_depth"),
    NFloat64("scan_end_crossline"),
    NFloat64("scan_end_inline"),
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
         No_Wedge = -1,
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
    NFloat64("inline_jaw_negative"),
    Padding(2),
    NFloat64("inline_jaw_positive"),
    Padding(2),
    NFloat64("crossline_jaw_negative"),
    Padding(2),
    NFloat64("crossline_jaw_positive"),
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
         No_Wedge = -1,
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
    NFloat64("inline_jaw_negative"),
    Padding(2),
    NFloat64("inline_jaw_positive"),
    Padding(2),
    NFloat64("crossline_jaw_negative"),
    Padding(2),
    NFloat64("crossline_jaw_positive"),
    
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
         No_Wedge = -1,
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
    NFloat64("inline_jaw_negative"),
    Repeater(2,UNInt8("raw")),
    NFloat64("inline_jaw_positive"),
    Repeater(2,UNInt8("raw")),
    NFloat64("crossline_jaw_negative"),
    Repeater(2,UNInt8("raw")),
    NFloat64("crossline_jaw_positive"),
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
    NFloat64("position_a_crossline"),
    NFloat64("position_a_inline"),
    NFloat64("position_a_depth"),
    NFloat64("position_b_crossline"),
    NFloat64("position_b_inline"),
    NFloat64("position_b_depth"),
    NFloat64("position_c_crossline"),
    NFloat64("position_c_inline"),
    NFloat64("position_c_depth"),
    NFloat64("position_d_crossline"),
    NFloat64("position_d_inline"),
    NFloat64("position_d_depth"),
    Repeater(10,UNInt8("raw")),
    NFloat64("scan_start_crossline"),
    NFloat64("scan_start_inline"),
    NFloat64("scan_start_depth"),
    NFloat64("scan_end_crossline"),
    NFloat64("scan_end_inline"),
    NFloat64("scan_end_depth"),
    Struct("data",
           SNInt16("length"),
           MetaRepeater(lambda ctx: ctx["length"],
                        StrictRepeater(2,NFloat64("data")))
           )
         
                            )

