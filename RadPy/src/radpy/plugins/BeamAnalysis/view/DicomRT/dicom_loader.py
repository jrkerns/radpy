'''
Created on Nov 7, 2010

@author: Steve
'''
import scipy, numpy 
import scipy.interpolate
import scipy.ndimage

from radpy.plugins.BeamAnalysis.view.beam_xml import Beam
from RTDoseRead import RTDose

class DicomBeam(Beam):
    
    def __init__(self):
        super(DicomBeam, self).__init__()
        
        
    def get_scan_descriptor(self):
        return ("Dicom_3D_Dose","")
    
    def does_it_match(self, args):
        
        for i,j in args.items():
            if i in ['scan_type','depth']:
                pass
            elif self.trait_get(i) != dict([(i,j)]):
                return False
        return True
    
    def overlap(self, a, b):
        """Takes 2-tuples a and b and returns True if the ranges overlap"""
        return a[1] > b[0] and a[0] < b[1]
        
    def get_beam(self, start, stop, axis_len):
        """Given two points, returns a beam object with a profile between them"""
        #Currently, this assumes that the profile will be either
        #inplane, crossplane or a depth dose (i.e. start and stop positions
        #are the same in two coordinates).
        #This function needs a good way to determine the abscissa axis values
        #in order to generalize to any linear scan.
        
        #Orient start-stop from negative to positive values
        scan_range = numpy.array([start[0]-stop[0],start[1]-stop[1],
                                  start[2]-stop[2]])
        if len(scan_range.nonzero()[0]) != 1:
            raise ValueError("Point to point scans are not able to matched in RadPy.")
        axis = scan_range.nonzero()[0][0]
        
        #Always orient the array from negative to positive coordinate values.
        if start[axis] > stop[axis]:
            start[axis], stop[axis] = stop[axis], start[axis]
            
        dcm_start = [min(self.Data.x_axis), min(self.Data.y_axis),
                     min(self.Data.z_axis)]
        dcm_stop = [max(self.Data.x_axis), max(self.Data.y_axis),
                     max(self.Data.z_axis)]
        for i in range(3):
            if not (self.overlap((start[i],stop[i]),(dcm_start[i], dcm_stop[i]))):
                raise ValueError("The scan range is outside the Dicom data range.")
            #Truncate if scan extends beyond dicom range
            if start[i] < dcm_start[i]:
                start[i] = dcm_start[i]
            if stop[i] > dcm_stop[i]:
                stop[i] = dcm_stop[i]
            
        
        
        #axis = scan_range.nonzero()[0][0]
#        abs_0 = dcm_start[axis]
#        abs_1 = dcm_stop[axis]
        abscissa = numpy.linspace(start[axis], stop[axis], axis_len)
#        abs_0 = start[axis]
#        abs_1 = stop[axis]
        
        
        x_interp = scipy.interpolate.interp1d(self.Data.x_axis, 
                                          numpy.arange(len(self.Data.x_axis)))
        y_interp = scipy.interpolate.interp1d(self.Data.y_axis, 
                                          numpy.arange(len(self.Data.y_axis)))
        z_indices = numpy.argsort(self.Data.z_axis)
        z_interp = scipy.interpolate.interp1d(self.Data.z_axis[z_indices], 
                                          numpy.arange(len(self.Data.z_axis)))
        
        
        x_values = x_interp(numpy.linspace(start[0],stop[0],axis_len))
        y_values = y_interp(numpy.linspace(start[1],stop[1],axis_len))
        z_values = z_interp(numpy.linspace(start[2],stop[2],axis_len))
        
#        axes = [x_values, y_values, z_values]
#        #abscissa = numpy.linspace(abs_0,abs_1,axis_len)
#        abscissa = axes[axis]
        
#        x_ind, y_ind, z_ind = numpy.mgrid[0:axis_len,0:axis_len,0:axis_len]
#        x_step = self.Data.x_axis[1] - self.Data.x_axis[0]
#        x_values =  x_ind*x_step + start[0]
        
        interp_vals = numpy.array([x_values,y_values,z_values])
        ordinate = scipy.ndimage.map_coordinates(self.Data.dose, interp_vals)
        
#        abscissa = self.Data.x_axis[27:89]
#        ordinate = self.Data.dose[27:89,38,24]
        
#        abscissa = []
#        i0 = numpy.sqrt(start[0]**2 + start[1]**2 + start[2]**2)
#        i1 = numpy.sqrt((stop[0] - start[0])**2 + (stop[1] - start[1])**2 +
#                         (stop[2] - start[2])**2)/len(ordinate)
#        for i in range(len(ordinate)):
#            abscissa.append(i0 + i*i1)

       
        
        #Create and initialize a new Beam object
        xml_beam = Beam()
        xml_beam.copy_traits(self)
        if axis == 2:  #Depth dose
            xml_beam.Data_Abscissa = -abscissa[::-1]
            xml_beam.Data_Ordinate = ordinate[::-1]
        else:
            xml_beam.Data_Abscissa = abscissa    
            xml_beam.Data_Ordinate = ordinate
        
        xml_beam.MeasurementDetails_StartPosition_x = start[0]
        xml_beam.MeasurementDetails_StopPosition_x = stop[0]
        xml_beam.MeasurementDetails_StartPosition_y = start[1]
        xml_beam.MeasurementDetails_StopPosition_y = stop[1]
        xml_beam.MeasurementDetails_StartPosition_z = start[2]
        xml_beam.MeasurementDetails_StopPosition_z = stop[2]
        xml_beam.filename = self.filename
        xml_beam.scan_type = xml_beam.get_scan_type()
        #xml_beam.set_label()
        return xml_beam
        
        
        

def load_dicom_data(infile):
    """Read in a file in RFB format and return a list of Beam objects"""
    
    
    
    f = RTDose(infile)
           
    xml_class = DicomBeam()
    xml_class.BeamDetails_CollimatorAngle = f.collimator_angle
    xml_class.BeamDetails_GantryAngle = f.gantry_angle
    xml_class.BeamDetails_Energy = float(f.energy)
    #xml_class.BeamDetails_RadiationDevice_Model = f.machine
    xml_class.Data = f
    #For right now, assume x is crossplane direction and y is inplane
    xml_class.BeamDetails_CrossplaneJawPositions_NegativeJaw = -f.coll_x_neg
    xml_class.BeamDetails_CrossplaneJawPositions_PositiveJaw = f.coll_x_pos
    xml_class.BeamDetails_InplaneJawPositions_NegativeJaw = -f.coll_y_neg
    xml_class.BeamDetails_InplaneJawPositions_PositiveJaw = f.coll_y_pos
    xml_class.BeamDetails_Particle = f.particle
    try:
        xml_class.BeamDetails_Wedge_Type = f.wedge_type
        xml_class.BeamDetails_Wedge_Angle = f.wedge_angle
    except:
        pass
    xml_class.MeasurementDetails_Isocenter_x = f.isocenter[0]
    xml_class.MeasurementDetails_Isocenter_y = f.isocenter[1]
    xml_class.MeasurementDetails_Isocenter_z = f.isocenter[2]
    xml_class.MeasurementDetails_MeasuringDevice_Manufacturer = f.meas_manu
    xml_class.MeasurementDetails_MeasuringDevice_Model = f.meas_model
    xml_class.BeamDetails_RadiationDevice_Vendor = f.rad_vend
    xml_class.BeamDetails_RadiationDevice_Model = f.rad_model
    xml_class.BeamDetails_RadiationDevice_SerialNumber = f.rad_serial
    xml_class.field_size = xml_class.get_field_size()
    xml_class.scan_type = xml_class.get_scan_type()
#    xml_class.Data_Abscissa = i.abscissa
#    xml_class.Data_Ordinate = i.ordinate
#    xml_class.initialize_traits()
#    b.append(xml_class)
#    f.close()
    return [xml_class]
    
