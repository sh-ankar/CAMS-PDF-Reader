# CAMS-Summary-PDF-Reader
Reads the CAMS+KFINTECH+FTAMIL CAS (Mutual Fund) Summary and provides a CSV output

Usage:
$python cams-summary-reader.py -f <camsfile.pdf> -p <password>

<camsfile.pdf> is the name of the CAS file (encrypted PDF) that you receive on email from CAMS. <password> is the password for the PDF. 

Output is <camsfile.pdf>.csv which will contain a csv of your main statement that you can import into your database or spreadsheet.

Dependencies:
this projects uses a wonderful pdf reader camelot-py. You will also need to install opencv-python. You can install dependencies using

$python -m pip install -r requirements.txt

NOTE: There is another version that reads the entire transaction statement. This version only reads the Summary report  
