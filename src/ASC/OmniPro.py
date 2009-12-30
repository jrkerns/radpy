import numpy

class OmniProFile(object):
    
    def __init__(self,Input_File):
        
        
        fp = file(Input_File,'r')
        text = []
        #text = fp.readlines()
        for line in fp:
            text.append(line.strip())
        fp.close()
        
            
        self.num_beams = int(text[0].lstrip('$NUMS'))

        self.beams = []
        #print 'count=' + str(text.count('$STOM'))
        for i in range(self.num_beams):
            #print i
            x = text.index('$STOM')
            y = text.index('$ENOM')

            if text[x:y].count('%TYPE OPD') or text[x:y].count('%TYPE WDD'):
                beamobject = OmniProDepthDose(text[x:y])
            elif text[x:y].count('%TYPE OPP') or text[x:y].count('%TYPE WDP'):
                beamobject = OmniProProfile(text[x:y])
                
            self.beams.append(beamobject)
            del text[x:y+1]

    #def MatchBeam(self,type,field_size,axis,ssd,depth=None):
    def MatchBeam(self,m):

        for i in self.beams:
            if m.type == 'Profile':
                if i.type == m.type and i.field_size == m.field_size \
                    and i.axis == m.axis and i.ssd == m.ssd \
                    and i.depth == m.depth:
                    return i
                    break
            else:
                if i.type == m.type and i.field_size == m.field_size \
                    and i.ssd == m.ssd:
                    return i
                    break
        return 'No Match'

    def findbeam(self,type,field_size,ssd,axis=None,depth=None):
        #not working for some reason.
        for i in self.beams:
            if i.type == type and i.field_size == field_size \
               and i.axis == axis and i.ssd == ssd and i.depth == depth:
                return i
                break

class OmniProDepthDose(object):

    def __init__(self,text):

        self.type = 'Depth Dose'
        self.z = []
        self.dose = []
        self.program = 'Measured'
        self.depth = None
        for i in text:
            if i.startswith('%SSD'):
                self.ssd = int(i.lstrip('%SSD'))
                break
        for i in text:
            if i.startswith('%FLSZ'):
                self.field_size = i.lstrip('%FLSZ').strip()
                break

        for i in text:
            if i.startswith('<'):
                temp = i.split(' ')
                self.z.append(eval(temp[2])/10.)
                self.dose.append(eval(temp[3].rstrip('>')))
                
        self.z = numpy.array(self.z)
        self.dose = numpy.array(self.dose)
        
class OmniProProfile(object):

    def __init__(self,text):

        self.type = 'Profile'
        self.x = []
        self.dose = []
        self.program = 'Measured'
        for i in text:
            if i.startswith('%SSD'):
                self.ssd = int(i.lstrip('%SSD'))
                break
        for i in text:
            if i.startswith('%FLSZ'):
                self.field_size = i.lstrip('%FLSZ').strip()
                break
        for i in text:
            if i.startswith('%DPTH'):
                self.depth = i.lstrip('%DPTH').strip()
                break

        for i in text:
            if i.startswith('%AXIS'):
                self.axis = i.lstrip('%AXIS').strip()
                if self.axis == 'X':
                    column = 0
                else:
                    column = 1
                break
                
        for i in text:
            if i.startswith('<'):
                temp = i.split(' ')
                self.x.append(eval(temp[column].lstrip('<'))/10.)
                self.dose.append(eval(temp[3].rstrip('>')))

        self.x = numpy.array(self.x)
        self.dose = numpy.array(self.dose)                
        