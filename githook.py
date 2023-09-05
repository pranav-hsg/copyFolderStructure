
import smtplib
from subprocess import check_output
import openpyxl
from openpyxl import Workbook
import openpyxl  
import xlrd
import xlwt
import os


filePath = "S:\projects\docs\projectk.xlsx"

# Get the git log --stat entry of the new commit
log = check_output(['git', 'log', '-1', '--stat', 'HEAD'])
strLogArr =  log.decode('utf8').strip().split("\n");
strLogArr = list(filter(lambda x: x!= '',strLogArr));
strLogArr = list(map(lambda x: x.strip(),strLogArr));
data = {
 "author_name" : strLogArr[1].split(" ")[1],
 "author_email" : strLogArr[1].split(" ")[2][1:-1],
 "commit_hash" : strLogArr[0].split(" ")[1],
 "date" : strLogArr[2].split("  ")[1].strip(),
 "comment" : strLogArr[3],
 "changes" : strLogArr[6]
}


if ( not os.path.exists(filePath)):    
    book = Workbook()  
    sheet = book.active
    sheet.append(list(data.keys()))
    book.save(filePath)
    
wb = openpyxl.load_workbook(filePath)  
sheet = wb.active  
sheet.append(list(data.values()))
wb.save(filePath);

