# Indent-Profiler
A laser scanning system jointly developed by KSU and AMI to profile indented wires used in prestressed concrete.

### To Do
	Calibration:
	  1.) Calculate measurement uncertainty from corrected precision cylinders.
      2.) Using this uncertainty, eliminate outliers that violate stdev bounds.
	  3.) Add documentation file that describes scanner uncertainty.

	fileIO.py:
	  1.) Make sure file handling can run on Windows/Unix systems

	utils.py
	  1.) Add coarse outlier removal based on precision cylinder scans.
	  2.) Add patching function to replace bad data points marked as np.nan. 
