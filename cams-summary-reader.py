import camelot
import csv
import sys, getopt

camsfile = ''
camspasswd = ''


#Collect arguments
# argv=sys.argv[1:]
try:
    opts, args = getopt.getopt(sys.argv[1:],"hf:p:",["camsfile=","password="])
except getopt.GetoptError:
    print ('cams-summary-reader.py -f <camsfile> -p <password>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print ('cams-summary-reader.py -f <camsfile> -p <password>')
        sys.exit()
    elif opt in ("-f", "--camsfile"):
        camsfile = arg
    elif opt in ("-p", "--password"):
        camspasswd = arg


#Header for CSV file
Header=["Folio", "Scheme","Unit Balance","NAV Date","NAV","Market Value","Registrar"]

#table 1 is the first page as it has a different layout for the the header section containing investor details
table1 = camelot.read_pdf(camsfile,password=camspasswd,pages="1",
    flavor='stream' ,table_regions=['28,590,568,82'],layout_kwargs={'detect_vertical': False})

#tables is thesecond page onwards as it uses full page tables
tables = camelot.read_pdf(camsfile,password=camspasswd,pages="2-end",
    flavor='stream',table_regions=['28,731,568,82'],layout_kwargs={'detect_vertical': False})

extract=[]
for row in table1[0].cells:
    rowline=[]
    for cell in row:
        rowline.append((cell.text).strip())
    extract.append(rowline)

reachedend=0

for pagenum in range(0, len(tables)):
    if reachedend: break
    for row in tables[pagenum].cells:
        if reachedend: break
        rowline=[]
        for cell in row:
            if (cell.text).strip()=="Total": 
                reachedend = 1 #no need to process further once we reach the "Total" row
                break
            rowline.append((cell.text).strip())
        if rowline[0] != "Folio No.":
            extract.append(rowline)

# Convert the pandas Df returned by camelot into a table so that its easy to use

for i in range(0, len(extract)):
    datacell = extract[i][0].strip()
    if extract[i][0].strip()=='':
        if (extract[i][1].strip()) != '':
            extract[i-1][1]= extract[i-1][1] + " " + extract[i][1]
            extract[i][1]=''
            continue

i=0
while i< len(extract):
    try:
        if extract[i][0].strip()=='' and extract[i][1].strip()=='': 
            del extract[i]
        if extract[i][0].strip() == 'Folio No.':
            del extract[i]
    except:
        break
    i+=1

i=0

#This code is needed as sometimes some scheme name overflows into 3rd line or the (INR) header in 2nd page is not captured correctly by camelot-py
while i< len(extract):
    try:
        if extract[i][0].strip()=='' and extract[i][1].strip()!='': 
            extract[i-1][1]= extract[i-1][1] + " " + extract[i][1]
            del extract[i]
        if extract[i][0].strip()=='' and extract[i][1].strip()=='': 
            # extract[i-1][1]= extract[i-1][1] + " " + extract[i][1]
            del extract[i]
    except:
        break
    i+=1
    
#write this to csv
with open(camsfile+".csv", 'w') as f:
    write = csv.writer(f) 
    write.writerow(Header) 
    write.writerows(extract) 
