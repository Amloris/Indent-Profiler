# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Indent Profiler: utils.py
-------------------------------------------------------------------------------
Aaron Robertson
FRA
March 2018
-------------------------------------------------------------------------------
File Description:
    Provides basic utilities that are used by multiple scripts in the Indent
profiler project. It mostly contains math operations and data visualization
tools.

Changelog:
04/11/18 - Updated file docstring. Added ArrayBounds(), GenerateHistogram().

-------------------------------------------------------------------------------
"""

#Libraries
import sys                       #Input/Output
import numpy as np               #Math
import matplotlib.pyplot as plt  #Visualization
import collections               #Named Tuples


'''Math Functions'''
'''-------------------------------------------------------------------------'''




'''Outlier Detection'''
'''-------------------------------------------------------------------------'''

def ArrayBounds(array, axis='row', index=0, get_avg=False):
    '''
    Determines the minimum and maximum values in a specified row or column 
    of a 2D array. Optionally, it can also return the average for the 
    specified row or column.

    Inputs
    ------
    array : ndarray
        A [nxm] numpy array.
    axis : str
        if 'row', array will be indexed based on rows. [Defualt]
        if 'col', array will be indexed based on columns.
    index : int
        The index of the row or column to evaluate.
    get_avg : bool, optional
        If False, only the max and min bounds are returned. [Default]
        If True, inlcudes the average in the returned tuple. 
        
    Outputs
    -------
    (min,max) : named tuple
        The minimum and maximum values for the row or column when get_avg=False
    (min,max,avg) : named tuple
        The minimum, maximum, and average value for the row or column when 
        get_avg=True.
    
    Notes
    -----
    A variable check is done for np.nan in this function as a defualt. Invalid
    data points for the Indent Profiler system are marked with np.nan. These
    points are not guaranteed to be filled in prior to the ArrayBounds()
    function call, thus, the user is warned about these points.
    '''
    
    #Array Index
    array_size = np.shape(array)

    #Check Array Boundaries
    if(axis != 'row' and axis != 'col'):
        print "ERROR: Invalid Axis Selected"
        sys.exit("TERMINATE:ARRAY_BOUNDS:INVALID_AXIS")
    if(axis == 'row' and index >= array_size[0]):
        print "ERROR: Array Bounds Exceeded"
        sys.exit("TERMINATE:ARRAY_BOUNDS:INVALID_BOUNDS")
    if(axis == 'col' and index >= array_size[1]):
        print "ERROR: Array Bounds Exceeded"
        sys.exit("TERMINATE:ARRAY_BOUNDS:INVALID_BOUNDS")
        
    #Evaluate Max and Min Values
    bounds = collections.namedtuple('bounds',['min','max','avg'])
    
    flag = 0
    if (axis == 'row'):
        if True in np.isnan(array[index,:]):flag=1
    if (axis == 'col'):
        if True in np.isnan(array[:,index]): flag=1
    if (flag == 1): print "WRN:ARRAY_BOUNDS:IS_NAN_DETECTED"
    
    if(axis == 'row'):
        array_slice = array[index,:]
        array_slice = array_slice[~np.isnan(array_slice)]
        min_val = np.min(array_slice)
        max_val = np.max(array_slice)
        if not get_avg: avg_val ='none'
        if get_avg:     avg_val = np.average(array_slice)
        bounds_vals = bounds(min_val, max_val, avg_val)
        return bounds_vals
    
    if(axis == 'col'):
        array_slice = array[:,index]
        array_slice = array_slice[~np.isnan(array_slice)]
        min_val = np.min(array_slice)
        max_val = np.max(array_slice)
        if not get_avg: avg_val ='none'
        if get_avg:     avg_val = np.average(array_slice)
        bounds_vals = bounds(min_val, max_val, avg_val)
        return bounds_vals

'''Data Visualization'''
'''-------------------------------------------------------------------------'''

def GenerateHistogram(array, bins=30, range=None):
    '''
    Draws a histogram of the provided data set.
    
    Input
    -----
    array : (n,)
        Either a single array or sequence of single arrays.
    bins : int, optional
        The number of bins the data will be devided into.
    range : tuple, optional
        The lower and upper range of the equally spaced bins. If not provided
        range is (array.min(),array.max()).
    '''
    
    plt.figure()
    plt.hist(array.flatten(), bins, range, edgecolor='black', zorder=3)
    plt.grid(True, linestyle = 'dashed',zorder=0)
    plt.ylabel('Frequency') 
    plt.show()
    
    return 0


if __name__ == "__main__":
    '''python utils.py
       Running this command will execute the test suite.
    '''
    
    test_array = np.array([[1,2,np.nan],[4,5,6]])
    vals = ArrayBounds(test_array,axis='row',index=0,get_avg=True)
    print vals.min, vals.max, vals.avg
    
    
    import fileIO
    data,header = fileIO.LoadData(fileIO.GetFile())
    GenerateHistogram(data)
