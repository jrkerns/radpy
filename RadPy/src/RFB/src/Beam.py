class Beam(object):

    def __init__(self):
        self.main_header = {}
        self.measurement_header = {}
        self.data_abscissa = []
        self.data_ordinate = []
        
    def get_field_size(self):
        """Return a string with field size information"""
        
        inline = self.main_header["inline_jaw_positive"] - \
                 self.main_header["inline_jaw_negative"]
        crossline = self.main_header["crossline_jaw_positive"] - \
                 self.main_header["crossline_jaw_negative"]
        return str(inline/10.).replace('.','_') + 'x' + \
            str(crossline/10.).replace('.','_')
                
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
         