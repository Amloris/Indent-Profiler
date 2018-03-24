# -*- coding: utf-8 -*-
#!/usr/bin/python3.6

'''
Indent Profiler: Testing File I/O
-------------------------------------------------------------------------------
Aaron Robertson
FRA
Mar 2018
-------------------------------------------------------------------------------
Program Description:
This program will test the functions used to import and export data files.
'''
 
'''Main Program'''
'''-------------------------------------------------------------------------'''
import sys
sys.path.insert(0, '/home/aaron/Documents/Github_Projects/Indent-Profiler')
from src import utils

def main():
    
    '''Program Control'''
    '''---------------------------------------------------------------------'''
    fname = "../../data/system_scans/raw/scans_wire/2018_3_23/WB/WB_1.csv"
    
    
    '''Manipulate Data'''
    data, scan_info = utils.LoadData(fname)            #Load File 


if __name__ == '__main__':
    main()
