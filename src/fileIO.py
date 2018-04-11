# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Indent Profiler: fileIO.py
-------------------------------------------------------------------------------
Aaron Robertson
FRA
March 2018
-------------------------------------------------------------------------------
File Description:
    Provides file handling utilities for the Indent Profiler project. Allows
for user specified directory and file selection, file loading and saving, and
path building.

Changelog:
04/05/18 - Updated header, added InitFileWindow(), changed deault file paths.
04/06/18 - Improved function docstrings. Added LoadData(), SaveData(), 
           LoadSplicedData(), and HeaderInfo class.
04/10/18 - Added VerifyFileNames().
-------------------------------------------------------------------------------
"""

#Libraries
import numpy as np                 #Math
import os                          #Input/Output
import sys                         #Input/Output
from Tkinter import Tk,TclError    #Input/Output
import tkFileDialog                #Input/Output


'''File Systems'''
'''-------------------------------------------------------------------------'''

def GetDir():
    '''Opens a window that allows a user to select a directory.
       Returns the directory path.
    '''
    
    #Set Window Attributes
    InitFileWindow()
    
    #Default Directory
    default_dir = "../data/system_scans/raw/scans_wire/2018_3_23/WB"
    
    #Get Specified Directory
    print "Select a data directory:"
    dir_name = str((tkFileDialog.askdirectory(initialdir="../",               \
                    title='Select Scan Directory')) or default_dir)
    dir_name = os.path.normpath(dir_name)
    print dir_name, '\n'

    return dir_name

def GetFile():
    '''Opens a window that allows a user to select a specific file.
       Returns the file path.
    '''
    
    #Set Window Attributes
    InitFileWindow()
    
    #Default Directory
    default_file = "../data/system_scans/raw/scans_wire/2018_3_23/WB/WB_1.csv"
    
    #Get Specified File
    print "Select a data file:"
    fname = str((tkFileDialog.askopenfilename(initialdir="../",               \
                 title = 'Select Data File', filetypes=[("CSV","*.csv"),      \
                 ("Text","*.txt")])) or default_file)  
    fname = os.path.normpath(fname)
    print fname, '\n'

    return fname

def InitFileWindow():
    '''Called before GetFile() and GetDir() in order to hide hidden elements
       on UNIX systems. The user has the option to toggle file hidding.
    '''
    
    root = Tk()
    root.withdraw()

    ###########################################################################
    # Attempting to hide hidden elements in UNIX file systems
    # http://grokbase.com/t/python/tkinter-discuss/158pthm66v/tkinter-file-dialog-pattern-matching
    # http://wiki.tcl.tk/1060
    ###########################################################################
    try:
         # Call a dummy dialog with an impossible option to initialize the file
         # dialog without really getting a dialog window; this will throw a
         # TclError, so we need a try...except :
         try:
             root.tk.call('tk_getOpenFile', '-foobarbaz')
         except TclError:
             pass
         # Now, set the magic variables accordingly
         root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
         root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
    except:
         pass
    ###########################################################################    
        
    return root
    

'''File Loading/Saving'''
'''-------------------------------------------------------------------------'''

def LoadData(fname, verify=True):
    '''
    Loads single segment scans and optionally checks for data integrity.
    
    Inputs
    ------
    fname : str
        The path to the file. The extension must be .txt or .csv to be loaded    
    verify : bool, optional
        If True, data integrity will be checked. [Default]
    
    Outputs
    -------
    header : class
        Header block data will be stored in a class for easy access.
    data : ndarray
        Scanner data is loaded into a [nxm] array. n = pts/rev, m = 800
        
    Notes
    -----
    A file extension check is provided in this function as a default. This 
    function will be used in multiple projects where file extensions are not
    guaranteed to be verfied prior to the LoadData() function call.
    '''
    
    #System Parameters
    cols_expected = 800       #Number of axial data points for the scanner

    #Set Extension
    filename, file_ext = os.path.splitext(fname)
    if (file_ext == '.txt'):
        delim = None
    elif (file_ext == '.csv'):
        delim = ','
    else:
        sys.exit("TERMINATE:LOAD_DATA:INVALID_EXTENSION")

    #Load Header
    header_length = 6
    header_index = np.arange(0, header_length)        #Header data rows

    with open(fname,'r') as fin:
        for i, line in enumerate(fin):
            if i in header_index:
                line_val = line.strip().split(delim)[-1]
                if i == 0: wire_profile     = str(line_val) 
                if i == 1: x_location       = float(line_val)
                if i == 2: total_sample_len = float(line_val)    
                if i == 3: pts_per_rev      = int(line_val)                   
                if i == 4: data_state       = str(line_val)
                if i == 5: time_stamp       = str(line_val)

    header = HeaderInfo(wire_profile, x_location, total_sample_len, \
                         pts_per_rev, data_state, time_stamp)

    #Load Data
    data = np.loadtxt(fname, delimiter=delim, skiprows=header_length)

    #Check Data Validity
    if verify:
        flag = 0
        if np.shape(data)[0] != header.pts_per_rev:
            flag = 1
            print "ERROR: Expected %i rows, got %i rows" \
                  %(header.pts_per_rev, np.shape(data)[0])
        if np.shape(data)[1] != cols_expected:
            flag = 1
            print "ERROR: Expected %i cols, got %i cols" \
                  %(cols_expected, np.shape(data)[1])
        if flag == 1:
            sys.exit("TERMINATE:LOAD_DATA:INVALID_ARRAY_BOUNDS")
        else:
            return data, header   
    else:
        return data, header

def SaveData():
    return 0

def LoadSplicedData():
    return 0

class HeaderInfo():
    '''Used to store the header data of scan files.'''
    
    def __init__(self, wire_profile, x_location, total_sample_length,
				 pts_per_rev, data_state, time_stamp):
        self.wire_profile = wire_profile
        self.x_location = x_location
        self.total_sample_length = total_sample_length
        self.pts_per_rev = pts_per_rev
        self.data_state = data_state
        self.time_stamp = time_stamp


'''Misc'''
'''-------------------------------------------------------------------------'''

def VerifyFileNames(dname, quiet=False):
    '''
    Verifies that the files follow the documented naming conventions.
    Used to check raw data directories that will be processed.
    
    Inputs
    ------
    dir_name : str
        The absolute path to the directory.
    quiet : bool, optional
        If False, all loading dialogue and errors will be displayed. [Default]
        If True, only critical errors will be displayed.
    '''
    
    #Get Parent Directory
    dir_parent = os.path.basename(dname)
    
    #Check Naming and Extensions
    if not quiet: print "Verifying Files: "   
    file_list = os.listdir(dname)       #Files contained in the directory
    if len(file_list) == 0:
        print "ERROR: No Files in Selected Directory"
        sys.exit("TERMINATE:VERIFY_FILE_NAMES:NO_FILES")
    
    flag, success = 0, 0
    for i in range(1,len(file_list)+1):
        check_fname = dir_parent+'_'+str(i)    #Expected file w/o extension
        if ((check_fname+'.csv') in file_list) or ((check_fname+'.txt') in file_list):
            success += 1
        else:
            print "ERROR: File Not Found (%s)" %check_fname
            flag = 1
    
    if flag == 1:
        print "ERROR: Invalid or Missing Files. Check Documentation."
        sys.exit("TERMINATE:VERIFY_FILE_NAMES:INVALID_FILE_NAMES")
    else:
        if not quiet: print "Passed (%i)\n" %success
        return 0


if __name__ == "__main__":
    '''python fileIO.py
       Running this command will execute the test suite.
    '''   

    dir_temp = GetDir()
    VerifyFileNames(dir_temp)
    
    file_temp = GetFile()
    LoadData(file_temp)
    
    #root.mainloop()
