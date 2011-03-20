# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

# This tree model class is based heavily on the tree model class in 
# "Rapid GUI Programming with Qt and Python" by Mark Summerfield.  
# Chapter 16 of that book in the section titled "Representing Tabular
# Data in Trees" provides the best description of the operation of this
# class.  
#
# Copyright (c) 2009 by Radpy.
# http://code.google.com/p/radpy/  

# Python system imports
import bisect
import string
import re
import os

# Major library imports
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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
        if self.column == 'File Name':
            return self
        else:
            parent = self.parent
            while parent.column != 'File Name':
                parent = parent.parent
            
        return parent

                
            
    

class LeafNode(object):

    def __init__(self, beam, parent=None):
        super(LeafNode, self).__init__()
        self.parent = parent
        #tree_path = beam.get_tree_path() + "|" + beam.get_scan_descriptor()
        self.fields = []
        self.row = 0
        #self.fields = fields
        self.fields.append(beam.get_scan_descriptor())
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
        record = "|".join(record[1:]) + "|" + \
            self.beam.get_scan_descriptor()
        return (record, self.beam)
        

    def field(self, column):
        assert 0 <= column <= len(self.fields)
        #return self.fields[column]
        return self.beam.get_scan_descriptor()
    
    def getFileBranch(self):
        """Returns the branch node that contains the entire data file."""
        """This function can be used to get the filename branch node.  
        One use is in the Save Data File action, which saves the file that 
        contains the currently selected node in the tree view."""
        
        parent = self.parent
        while parent.column != 'File Name':
            parent = parent.parent
            
        return parent
    

class TreeModel(QAbstractItemModel):

    def __init__(self, headers, parent=None):
        super(TreeModel, self).__init__(parent)
        self.columns = 0
        self.root = BranchNode("","")
        self.headers = headers


    def load(self, filename, nesting, columns, separator = "|"): 
        assert nesting > 0
        self.nesting = nesting
        #self.root = BranchNode("", "")
        exception = None
        self.filepath = filename
        self.filename = os.path.basename(filename).split('.')[0]
        extension = os.path.basename(filename).split('.')[-1]
        try:
            if extension == 'rfb':
                data = load_rfb_data(filename)
            elif extension == 'xml':
                data = load_xml_data(filename)
            elif extension == 'dcm':
                data = load_dicom_data(filename)
            
            for beam in data:
                beam.set_label()
                self.addRecord(beam, False)
        except IOError, e:
            exception = e
        finally:
            
            self.reset()
            
            if exception is not None:
                raise exception
    
    def removeRecord(self, index):
        
        root_reset = False
        row = index.row()
        beam = self.nodeFromIndex(index)
        if beam.parent is None:
            return True
        else:           
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
        fields = (self.filename + "|" + beam.get_tree_path()).split("|")
        for i in range(self.nesting):
            key = fields[i].lower()
            branch = root.childWithKey(key)
            if branch is not None:
                root = branch
            else:                
                branch = BranchNode(fields[i],self.headers[i])
                if self.headers[i] == 'File Name':
                    branch.filename = self.filepath

                parent_index = self.createIndex(root.row,0,root)
                self.beginInsertRows(parent_index,len(root),len(root))
                root.insertChild(branch)
                self.endInsertRows()

                root = branch
        assert branch is not None

        item = LeafNode(beam, branch)
        self.columns = max(self.columns, 1)

        

        parent_index = self.createIndex(branch.row,0,branch)
        self.beginInsertRows(parent_index,len(branch),len(branch))
        branch.insertChild(item)
        
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
        