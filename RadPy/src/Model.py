# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

#This tree model class is based heavily on the tree model class in 
#"Rapid GUI Programming with Qt and Python" by Mark Summerfield.  
#Chapter 16 of that book in the section titled "Representing Tabular
#Data in Trees" provides the best description of the operation of this
#class.  

# Python system imports
import bisect
import string
import re
import os

# Major library imports
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Program specific imports
from RFB.hdf5 import load_multi_data

KEY, NODE = range(2)



class BranchNode(object):
    #This represents a branch of the tree model.
    #The code is essentially unchanged from the code in the
    #Summerfield book.
    #TODO: enable activating a branch node to add all of its
    #tree nodes to active scan window.
    
    def __init__(self, name, column, parent=None):
        #super(BranchNode, self).__init__(parent)
        super(BranchNode, self).__init__()
        self.name = name
        self.parent = parent
        self.column = column
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
        i = bisect.bisect_left(self.children, (key, None))
        if i < 0 or i >= len(self.children):
            return None
        if self.children[i][KEY] == key:
            return self.children[i][NODE]
        return None


    def insertChild(self, child):
        child.parent = self
        bisect.insort(self.children, (child.orderKey(), child))


    def hasLeaves(self):
        if not self.children:
            return False
        return isinstance(self.children[0], LeafNode)


class LeafNode(object):

    def __init__(self, beam, parent=None):
        super(LeafNode, self).__init__()
        self.parent = parent
        #tree_path = beam.get_tree_path() + "|" + beam.get_scan_descriptor()
        self.fields = []
        
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
        self.filename = os.path.basename(filename).split('.')[0]
        try:
            data = load_multi_data(filename)
            for beam in data:
                self.addRecord(beam, False)
        except IOError, e:
            exception = e
        finally:
            
            self.reset()
            
            if exception is not None:
                raise exception


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
                root.insertChild(branch)
                root = branch
        assert branch is not None
        item = beam
        self.columns = max(self.columns, 1)
        branch.insertChild(LeafNode(item, branch))
        if callReset:
            self.reset()


    def asRecord(self, index):
        leaf = self.nodeFromIndex(index)
        if leaf is not None and isinstance(leaf, LeafNode):
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
            return QVariant(int(Qt.AlignTop|Qt.AlignLeft))
        if role != Qt.DisplayRole:
            return QVariant()
        node = self.nodeFromIndex(index)
        assert node is not None
        if isinstance(node, BranchNode):
            return QVariant(node.toString()) \
                if index.column() == 0 else QVariant(QString(""))
        return QVariant(node.field(index.column()))


    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and \
           role == Qt.DisplayRole:
            assert 0 <= section <= len(self.headers)
            return QVariant(self.headers[section])
        return QVariant()


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
        regex = re.compile('\d*')
        try:
            l = int(regex.findall(left.data().toString())[0])
            r = int(regex.findall(right.data().toString())[0])
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
        
    def columnCount(self, *args, **kwds):
        return self.sourceModel().columnCount(*args, **kwds)