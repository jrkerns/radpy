from enthought.traits.api import HasTraits, Array, Dict, String

class Beam(HasTraits):
    """Class that defines the data model for a scan.
    This needs to be updated when a universal data format
    is decided upon."""
    
    main_header = Dict()
    measurement_header = Dict()
    data_abscissa = Array()
    data_ordinate = Array()
    label = String()
        
    def set_label(self):
        self.label = '|'.join([self.get_tree_path(),self.get_scan_descriptor()]) 
           
    def get_field_size(self):
        """Return a string with field size information"""
        
        inline = int(self.main_header["inline_jaw_positive"] - \
                 self.main_header["inline_jaw_negative"])
        crossline = int(self.main_header["crossline_jaw_positive"] - \
                 self.main_header["crossline_jaw_negative"])
        return str(inline) + 'x' + str(crossline)
            
    def get_machine(self):
        """Return a string with the machine beam data is from"""
        
        return self.main_header["rad_device"]
    
    def get_energy(self):
        """Return a string with the energy and particle type"""
        #Returns a string with the usual energy/particle specification,
        #e.g. 6X, 18E.
        energy = str(int(self.main_header["energy"]))
        if self.main_header["particle"] == 'Photon':
            particle = 'X'
        elif self.main_header["particle"] == 'Electron':
            particle = 'E'
        else:
            particle = ''
        return energy + particle
    
    def get_tree_path(self):
        """Returns a string with parameters used to populate the GUI tree"""
        #Seperator is |.  Uses machine name, energy and field size to tell
        #the GUI tree view where on the tree this beam belongs.
        
#        return self.get_machine() + "|" + self.get_energy() + "|" + \
#                self.get_field_size()
        return '|'.join([self.get_machine(), self.get_energy(),self.get_field_size()])
                
    def get_scan_type(self):
        """Determine the type of scan by comparing start and end positions"""
        
        scan_range = [self.measurement_header["scan_start_crossline"] - \
                        self.measurement_header["scan_end_crossline"],
                      self.measurement_header["scan_start_inline"] - \
                        self.measurement_header["scan_end_inline"],
                      self.measurement_header["scan_start_depth"] - \
                        self.measurement_header["scan_end_depth"]]
        scan_types = ["Crossline Profile", "Inline Profile", "Depth Dose"]
        if scan_range.count(0.0) != 2:
            return "Point to Point"
        else:
            return scan_types[[i for i, j in enumerate(scan_range) \
                               if j !=0][0]]
    

    def get_scan_descriptor(self):
        """Return a string with scan type and position information"""
        
        scan_type = self.get_scan_type()
        if scan_type == "Crossline Profile":
            return "Crossplane_Profile_" + \
                str(self.measurement_header["scan_end_depth"]/10.)
        elif scan_type == "Inline Profile":
            return "Inplane_Profile_" + \
                   str(self.measurement_header["scan_end_depth"]/10.)
        else:
            return "Depth_Dose"
         
    def get_collimator(self, direction="crossline"):
        
        if direction == "crossline":
            return self.main_header["crossline_jaw_positive"] - \
                 self.main_header["crossline_jaw_negative"]
        elif direction == "inline":
            return self.main_header["inline_jaw_positive"] - \
                 self.main_header["inline_jaw_negative"]
        else:
            pass
        
    def get_equiv_square(self):
        
        x = self.get_collimator("crossline")
        y = self.get_collimator("inline")
        return 4 * x * y/(2 * x + 2 * y)