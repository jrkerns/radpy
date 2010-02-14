from rfb import omnipro_file
import csv
import tables

def create_hdf_file(infile, outfile):
    """Read in a file in RFB format and output it to HDF5 format"""
    h5file = tables.openFile(outfile, mode = "w", title = "omnipro")
    f = open(infile,'rb')
    a = omnipro_file.parse(f.read())
    f.close()
    
    rad_dev = h5file.createGroup(h5file.root,
                str(a[0].main_header["rad_device"]),
                str(a[0].main_header["rad_device"]))
    for i, j in enumerate(a):
        try: 
            group = h5file.createGroup(rad_dev, j.get_field_size(),
                                       j.get_field_size())
        except:
            group = h5file.getNode(rad_dev, j.get_field_size())
        scan = h5file.createGroup(group, 'Scan'+str(i), 
                                  j.get_scan_descriptor())
        h5file.createArray(scan, 'x', j.data_abscissa, 'x')
        h5file.createArray(scan, 'y', j.data_ordinate, 'y')
        
        
    h5file.close()      

def load_multi_data(infile):
    """Read in a file in RFB format and return a list of Beam objects"""
    f = open(infile,'rb')
    a = omnipro_file.parse(f.read())
    f.close()
    return a


def beam_csv_dump(infile, outfile):
    """Read in a file in RFB format and dump header info to a CSV file"""
    
    f = open(infile,'rb')
    a = omnipro_file.parse(f.read())
    f.close()

    f = open(outfile,'wb')
    writer = csv.writer(f)
    keys = []
    
    #main_keys and measurement_keys are lists of header fields to be
    #dumped into the csv file.
    
    main_keys = ['rad_device', 'energy', 'particle',
                 'inline_jaw_negative', 'inline_jaw_positive',
                 'crossline_jaw_negative', 'crossline_jaw_positive',
                 'gantry_angle', 'wedge_type', 'wedge_angle','SSD']
    measurement_keys = ['peff_offset', 'modified_date',
                        'scan_start_crossline', 'scan_start_inline',
                        'scan_start_depth', 'scan_end_crossline',
                        'scan_end_inline', 'scan_end_depth']
    
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

def compare_raw_fields(a,b):
    for i in a.measurement_header.keys():
        if i.startswith("raw"):
            print i, b.measurement_header[i] == \
                  a.measurement_header[i]
    
if __name__ == "__main__":
    #create_hdf_file('f:/rfb/tests/test1.rfb','f:/rfb/tests/test1.h5')
    #create_hdf_file('f:/rfb/tests/test2.rfb','f:/rfb/tests/test2.h5')
    #create_hdf_file('f:/rfb/tests/test3.rfb','f:/rfb/tests/test3.h5')
    #create_hdf_file('f:/rfb/tests/test4.rfb','f:/rfb/tests/test4.h5')
    #create_hdf_file('f:/rfb/tests/test5.rfb','f:/rfb/tests/test5.h5')
    a=load_multi_data('f:/radlab/src/rfb/unit tests/test1.rfb')
    #a=load_multi_data('c:/testing.rfb')
    #for i in a:
    #    print i.main_header["energy"]
    