This directory stores the raw data that is generated from the scanner.
The sections below summarize the layout of the directory, file naming
conventions, and data stuctures of the raw files.

Section 1: Directory Structure and File Naming
----------------------------------------------

```bash 
.
└── raw
    ├── scans_calibration
    │   ├── date_cal_1
    │   │   ├── Cal_1.csv
    │   │   └── Cal_2.csv
    │   └── date_cal_2
    │       └── Cal_3.csv
    └── scans_wire
        ├── date_scan_1
        │   ├── Scan_1
        │   │   ├── WireID_1.csv
        │   │   ├── WireID_2.csv
        │   │   ├── WireID_3.csv
        │   │   └── WireID_4.csv
        │   └── Scan_2
        │       ├── WireID_1.csv
        │       ├── WireID_2.csv
        │       ├── WireID_3.csv
        │       └── WireID_4.csv
        └── date_scan_2
            └── Scan_3
                ├── WireID_1.csv
                └── WireID_2.csv
```

Notes

    Directory Info:
      1.) /raw, /scans_calibration, and /scans_wire  are all static directories
      2.) /date_cal_# and /date_scan_# use the following naming syntax
              Syntax : /year_month_date
              Example: A scan taken on March 21st, 2018 would be given the
                       directory name,  /2018_3_21

    File Naming (Calibration):
      1.) Calibration files are single segment scans. Thus, no subdirectories
          are needed.
      2.) Each calibration file should be given an appropriate name identifier
          with a .csv extension. The file desciptor in the header should
          indicate which precision cylinder blank was used.

    File Naming (Wires):
      1.) Wire scans are multi-segment scans. Thus subdirectories are
          necessary to differentiate between individual scans.
      2.) Each specimen should be given an individual subdirectory with an
          appropriate ID, eg. /Scan_1.
      3.) Since a wire scan can be composed of multiple segments an additional
          identifier is given prior to the file extension. The x-position
          section in the header indicates where the scan segment physcially
          begins.
              Example: WireID_1.csv   (The first scan segment)
                       WireID_2.csv   (The second scan segment)

Section 2: Data Structures
--------------------------

/Fill this out when we settle on a permanent data structure.
