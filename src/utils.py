#------------------------------------------------------------------------------
#Utility for commonly used functions
#------------------------------------------------------------------------------
import os
import numpy as np

'''File I/O'''
'''-------------------------------------------------------------------------'''
def LoadData(fname):
    '''Load data from a text file or csv file generated by the indent profiler.

       Inputs:
           fname = The relative path to the data file.
                   The extension of the data file must be '.txt' or '.csv'.
       Outputs:
           data      = A [nxm] array of floating point numbers.
           scan_info = The header info of the data file, stored as a struct.
    '''

    #Set Extension
    filename, file_ext = os.path.splitext(fname)
    if (file_ext == '.txt'):
        delim = None
    elif (file_ext == '.csv'):
        delim = ','
    else:
        print "ERROR: File Extension Requirement Not Met"
        return 0

    #Load Header
    header_length = 6
    header_index = np.arange(0, header_length)    #The rows which contain heade

    with open(fname,'r') as fin:
        for i, line in enumerate(fin):
            if i in header_index:
                line_val = line.strip().split(delim)[-1]
                if i == 0:
                    wire_profile     = str(line_val)
                if i == 1:
                    x_location       = float(line_val)
                if i == 2:
                    total_sample_len = float(line_val)
                if i == 3:
                    pts_per_rev      = int(line_val)
                if i == 4:
                    data_state       = str(line_val)
                if i == 5:
                    time_stamp       = str(line_val)

    scan_info = ScanInfo(wire_profile, x_location, total_sample_len, \
                         pts_per_rev, data_state, time_stamp)

    #Load Data
    data = np.loadtxt(fname, delimiter=delim, skiprows=header_length)

    return data, scan_info


class ScanInfo():
    def __init__(self, wire_profile, x_location, total_sample_length,
				 pts_per_rev, data_state, time_stamp):
        self.wire_profile = wire_profile
        self.x_location = x_location
        self.total_sample_length = total_sample_length
        self.pts_per_rev = pts_per_rev
        self.data_state = data_state
        self.time_stamp = time_stamp



'''Outlier Detection'''
'''-------------------------------------------------------------------------'''

def Bounds(array, axis='row', index=0, get_avg=False):
    '''Determines the minimum and maximum values in a specified row or column 
       of a 2D array. Optionally, it can also return the average for the 
       specified row or column.

       Inputs:
           array   = An [nxm] numpy array
           axis    = 'row' or 'col', row is selected as the default
           index   = The index of the row or column to evaluate
           get_avg = Adds the average to the returned tuple, default = False

       Outputs:
           (min,max) = The minimum and maximum values for the row or column
                       when get_avg=False
           (min,max,avg) = The minimum, maximum, and average value for the 
                       specified row or column when get_avg=True
    '''
    #Array Index
    array_size = np.shape(array)

    #Check Array Boundaries
    if(axis == 'row' and index >= array_size[0]):
        print "ERROR: Array Bounds Exceeded"
        return 0
    if(axis == 'col' and index >= array_size[1]):
        print "ERROR: Array Bounds Exceeded"
        return 0
    if(axis != 'row' and axis != 'col'):
        print "ERROR: Invalid Axis Selected"
        return 0

    #Evaluate Max and Min Values
    if(axis == 'row'):
        min_val = np.min(array[index,:])
        max_val = np.max(array[index,:])
        if not get_avg:
            return (min_val,max_val)
        avg_val = np.average(array[index,:])
        return (min_val,max_val,avg_val)
    if(axis == 'col'):
        min_val = np.min(array[:,index])
        max_val = np.max(array[:,index])
        if not get_avg:
            return (min_val,max_val)
        avg_val = np.average(array[:,index])
        return (min_val,max_val,avg_val)

if __name__ == "__main__":
    import os
    import numpy as np
