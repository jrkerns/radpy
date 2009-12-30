'''
Created on Jul 13, 2009

@author: Stephen_Terry
'''

from RTDoseRead import RTDose
import numpy
import pylab

if __name__ == '__main__':
    a=RTDose('C:/Documents and Settings/fpo9697/Desktop/Shared/3d_dose_wedge.dcm')
    #print numpy.max(a.dose)
    #tmp = numpy.where(a.dose == numpy.max(a.dose))
    #print tmp
    #print a.x_axis[tmp[0]],a.y_axis[tmp[1]],a.z_axis[tmp[2]]
    #print a.get_dose_value(a.x_axis[tmp[0]],a.y_axis[tmp[1]],a.z_axis[tmp[2]])
    pylab.plot(a.y_axis,a.get_dose_profile())

    