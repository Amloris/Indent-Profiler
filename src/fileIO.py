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
04/08/18 - Updated header, added InitFileWindow()
-------------------------------------------------------------------------------
"""



#Libraries
import numpy as np                 #Math
import os                          #Input/Output
from Tkinter import Tk,TclError    #Input/Output
import tkFileDialog                #Input/Output


def GetDir():
    '''Opens a window that allows a user to select a directory.'''
    
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
    '''Opens a window that allows a user to select a specific file.'''
    
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
    

def VerifyFileNames(dir_name):
    '''Verfies that the files follow the documented naming conventions.
    
       Input:
           dir_name = The absolute path to the directory [str]
    '''
    
    #Get Parent Directory
    dir_parent = os.path.basename(dir_name)
    
    #Check Naming and Extensions
    print "Verifying Files: "
    
    file_list = os.listdir(dir_name)       #Files contained in the directory
    if len(file_list) == 0:
        print "ERROR: No Files in Selected Directory"
        return 1
    
    flag = 0
    success = 0
    for i in range(1,len(file_list)+1):
        check_fname = dir_parent+'_'+str(i)    #Expected file w/o extension
        if ((check_fname+'.csv') in file_list) or ((check_fname+'.txt') in file_list):
            success += 1
        else:
            print "ERROR: File Not Found (%s)" %check_fname
            flag = 1
    
    if flag == 1:
        print "Invalid or Missing Files. Check Documentation."
        return 1
    else:
        print "Passed (%i)" %success
        return 0


if __name__ == "__main__":
    '''python fileIO.py
       Running this command will execute the test suite.
    '''

    InitFileWindow()    

    GetDir()
    GetFile()
    
    #root.mainloop()
