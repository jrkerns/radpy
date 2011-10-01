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

# This tree model class is based heavily on the tree model class in 
# "Rapid GUI Programming with Qt and Python" by Mark Summerfield.  
# Chapter 16 of that book in the section titled "Representing Tabular
# Data in Trees" provides the best description of the operation of this
# class.  

# Python system imports
import re
import os
import fnmatch

# Major library imports
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import lxml


# Program specific imports
from RFB.rfb_loader import load_rfb_data
from xml_loader import load_xml_data
from DicomRT.dicom_loader import load_dicom_data

KEY, NODE = range(2)



class BranchNode(object):
    #This represents a branch of the tree model.
    #The code is essentially unchanged from the code in the
    #Summerfield book.
    
    def __init__(self, name, column, parent=None):
        #super(BranchNode, self).__init__(parent)
        super(BranchNode, self).__init__()
        self.name = name
        self.parent = parent
        self.column = column
        self.row = 0
        self.children = []
    

    def orderKey(self):
        
#        if self.column == 'Machine':
#            return self.name.lower()
#        elif self.column == 'Energy':
#            return int(self.name.strip(string.ascii_letters))
#        elif self.column == 'Field Size':
#            x, y = [int(i.split("_")[0]) + float(i.split("_")[1])/10 for i in self.name.split('x')]
#            return 2 * x * y / (x + y)
        return self.name.lower()


    def toString(self):
        return self.name


    def __len__(self):
        return len(self.children)
    

    def childAtRow(self, row):
        assert 0 <= row < len(self.children)
        return self.children[row][NODE]
        

    def rowOfChild(self, child):
        for i, item in enumerate(self.children):
            if item[NODE] == child:
                return i
        return -1


    def childWithKey(self, key):
        if not self.children:
            return None
#        i = bisect.bisect_left(self.children, (key, None))
        i = -1
        for n,child in enumerate(self.children):
            if child[KEY] == key:
                i = n
                break

        if i < 0 or i >= len(self.children):
            return None
        if self.children[i][KEY] == key:
            return self.children[i][NODE]
        return None


    def insertChild(self, child):
        child.parent = self
#        row = bisect.bisect_left(self.children, (child.orderKey(), child))
#        bisect.insort(self.children, (child.orderKey(), child))
#        return row
        row = len(self.children)
        child.row = row
        self.children.append((child.orderKey(), child))
        
        


    def hasLeaves(self):
        if not self.children:
            return False
        return isinstance(self.children[0], LeafNode)
    
    def asRecord(self):
        """Find all leaf nodes in this branch and return them in list form."""
        all_leaves = []
        for text,node in self.children:
            if isinstance(node, LeafNode):
                all_leaves.append(node.asRecord())
            else: 
                for leaf in node.asRecord():
                    all_leaves.append(leaf)
            
        return all_leaves
    
    def getFileBranch(self):
        """Returns the branch node that contains the entire data file."""
        """This function can be used to get the filename branch node.  
        One use is in the Save Data File action, which saves the file that 
        contains the currently selected node in the tree view."""
        if self.parent.parent == None:
            return self
        else:
            parent = self.parent
            while True:
                if hasattr(parent, 'filename'):
                    return parent
                parent = parent.parent

                
            
    

class LeafNode(object):

    def __init__(self, beam, parent=None):
        super(LeafNode, self).__init__()
        self.parent = parent
        #tree_path = beam.get_tree_path() + "|" + beam.get_scan_descriptor()
        self.fields = []
        self.row = 0
        #self.fields = fields
        profile_type, depth = beam.get_scan_descriptor()
        self.fields.append(profile_type)
        self.fields.append(depth)
        self.beam = beam


    def orderKey(self):
        return u"\t".join(self.fields).lower()

    def toString(self, separator="\t"):
        return separator.join(self.fields)


    def __len__(self):
        return len(self.fields)


    def asRecord(self):
        record=[]
        branch=self.parent
        
        #Walk up the tree model, inserting the string representation of each
        #branch into the record list.  (e.g. ['filename', '6X', '40x40'])
        #This is used to create the plot title.
        while branch is not None:
            record.insert(0,branch.toString())
            branch=branch.parent
            
        assert record and not record[0]
        profile_type, depth = self.beam.get_scan_descriptor()
        record = "|".join(record[1:]) + "|" + profile_type + "|" + depth
        return (record, self.beam)
        

    def field(self, column):
        assert 0 <= column <= len(self.fields)
        return self.fields[column]
        #return self.beam.get_scan_descriptor()
    
    def getFileBranch(self):
        """Returns the branch node that contains the entire data file."""
        """This function can be used to get the filename branch node.  
        One use is in the Save Data File action, which saves the file that 
        contains the currently selected node in the tree view."""
        
        if self.parent.parent == None:
            return self
        else:
            parent = self.parent
            while True:
                if hasattr(parent, 'filename'):
                    return parent
                parent = parent.parent
    

class TreeModel(QAbstractItemModel):

    def __init__(self, headers, parent=None):
        super(TreeModel, self).__init__(parent)
        self.columns = 0
        self.root = BranchNode("","")
        self.headers = headers


    def load(self, filename, nesting, columns, separator = "|", progress=None): 
        assert nesting > 0
        self.nesting = nesting
        #self.root = BranchNode("", "")
        exception = None
        self.filepath = filename
        if os.path.isdir(filename):
            filenames = []
            rootPath = filename
            self.filename = os.path.split(os.path.basename(filename))[-1]
            patterns = ['*.rfb','*.dcm','*.xml'] 
 
            for root, dirs, files in os.walk(rootPath):
                for p in patterns:
                    for file in fnmatch.filter(files, p):
                        
                        filenames.append((os.path.join(root, file)))
        
        else:
            filenames = [filename]
            #self.filename = os.path.basename(filename).split('.')[0]
            self.filename = os.path.splitext(os.path.basename(filename))[0]
            
        if progress:
            progress.setWindowTitle('Loading...')
            progress.setMinimum(0)
            progress.setMaximum(len(filenames))
            progress.show()
        
        for value, file in enumerate(filenames):
            
            if progress:
                progress.setValue(value)
            #extension = os.path.basename(file).split('.')[-1]
            extension = os.path.splitext(file)[-1]
            
            try:
                if extension == '.rfb':
                    data = load_rfb_data(file)
                elif extension == '.xml':
                    data = load_xml_data(file)
                elif extension == '.dcm':
                    data = load_dicom_data(file)
                
                for beam in data:
                    beam.set_label()
                    beam.filename = self.filename
                    self.addRecord(beam, False)
            
            #except (IOError, ValueError):
            except Exception as error:
                
                QMessageBox.warning(None, "File Read Error", ("Error reading "  
                + file + ".  " + str(error)),
                buttons=QMessageBox.Ok)        
            
            
        self.reset()
    
    def removeRecord(self, index):
        
        root_reset = False
        row = index.row()
        beam = self.nodeFromIndex(index)
        if beam.parent is None or beam.parent == self.root:
            root_reset = True
        if beam.parent is not None:
#            return True
#        else:           
            parent = self.parent(index)    
            self.beginRemoveRows(parent,row,row)
            
            beam.parent.children.pop(row)
            self.endRemoveRows()
            if len(beam.parent.children) == 0:
                root_reset = self.removeRecord(parent)
        return root_reset

    def addRecord(self, beam, callReset=True):
        #assert len(fields) > self.nesting
        root = self.root
        branch = None
        #fields = (beam.filename + "|" + beam.get_tree_path()).split("|")
        fields = (beam.filename + "|" + beam.get_tree_path()).split("|")
        for i in range(self.nesting):
            key = fields[i].lower()
            branch = root.childWithKey(key)
            if branch is not None:
                root = branch
            else:                
                branch = BranchNode(fields[i],self.headers[0])
                if i == 0: 
                    branch.filename = self.filepath

                parent_index = self.createIndex(root.row,0,root)
                self.beginInsertRows(parent_index,len(root),len(root))
                root.insertChild(branch)
                self.endInsertRows()

                root = branch
        assert branch is not None

        #item = LeafNode(beam, branch)
        items = fields[self.nesting:]
        #self.columns = max(self.columns,1)
        self.columns = max(self.columns, len(items))
        

        parent_index = self.createIndex(branch.row,0,branch)
        self.beginInsertRows(parent_index,len(branch),len(branch))
        branch.insertChild(LeafNode(beam, branch))
        
        self.endInsertRows()
        
        if callReset:
            self.reset()


    def asRecord(self, index):
        leaf = self.nodeFromIndex(index)
        if leaf is not None: #and isinstance(leaf, LeafNode):
            return leaf.asRecord()
        return []


    def rowCount(self, parent):
        node = self.nodeFromIndex(parent)
        if node is None or isinstance(node, LeafNode):
            return 0
        return len(node)


    def columnCount(self, parent):
        return self.columns


    def data(self, index, role):
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignTop|Qt.AlignLeft)
        
        if role == Qt.DecorationRole:
            node = self.nodeFromIndex(index)
            if node is None:
                return None
            if isinstance(node, LeafNode) and index.column() == 0:
                filename = os.path.join('./radpy/images',
                                        node.field(0)+'.png')
                pixmap = QPixmap(filename)
                if pixmap.isNull():
                    return None
                return pixmap
                           
        if role != Qt.DisplayRole:
            return None
        node = self.nodeFromIndex(index)
        assert node is not None

        if isinstance(node, BranchNode):
            return node.toString() \
                if index.column() == 0 else ""

        return node.field(index.column())


    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and \
           role == Qt.DisplayRole:
            assert 0 <= section <= len(self.headers)
            return self.headers[section]
        return None


    def index(self, row, column, parent):
        assert self.root
        branch = self.nodeFromIndex(parent)
        assert branch is not None
        return self.createIndex(row, column,
                                branch.childAtRow(row))


    def parent(self, child):
        node = self.nodeFromIndex(child)
        if node is None:
            return QModelIndex()
        parent = node.parent
        if parent is None:
            return QModelIndex()
        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()
        row = grandparent.rowOfChild(parent)
        assert row != -1
        return self.createIndex(row, 0, parent)


    def nodeFromIndex(self, index):
        return index.internalPointer() \
            if index.isValid() else self.root

class ProxyModel(QSortFilterProxyModel):
    #Wraps the tree model and provides custom sorting for each column
    def __init__(self, parent=None):
        super(ProxyModel, self).__init__(parent)
        
    def lessThan(self, left, right):
        """ Provides custom sorting by field size (10x10 before 40x40) """
        regex = re.compile('\d*')
        try:
            l = int(regex.findall(left.data())[0])
            r = int(regex.findall(right.data())[0])
            if l < r:
                return False
            else:
                return True
        except ValueError:
            return right < left
        
    def load(self, *args, **kwds):
        return self.sourceModel().load(*args, **kwds)
    
    def asRecord(self, index):
        return self.sourceModel().asRecord(self.mapToSource(index))
        
    def nodeFromIndex(self, index):
        return self.sourceModel().nodeFromIndex(self.mapToSource(index))
    
    def columnCount(self, *args, **kwds):
        return self.sourceModel().columnCount(*args, **kwds)
    
    def addRecord(self, *args, **kwds):
        return self.sourceModel().addRecord(*args, **kwds)
    
    def removeRecord(self, index):
        return self.sourceModel().removeRecord(self.mapToSource(index))
    
