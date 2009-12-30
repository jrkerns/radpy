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
    