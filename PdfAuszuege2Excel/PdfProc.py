import os as os
import pdfplumber
import re
import pandas as pd
from tabula import convert_into, convert_into_by_batch, read_pdf
from tabulate import tabulate
import camelot
import ghostscript
import locale
import csv
from dateutil.parser import parse

ROOT_PATH = r'C:\Users\quocb\OneDrive\Dokumente\Finanz\ING\Kontoauszuege'
TEMP_PATH = r'C:\Temp\Pdf2Txt\ING'
# ROOT_PATH = r'C:\Users\quocb\OneDrive\Dokumente\Finanz\Comdirect_Download\Finanzreport'
# TEMP_PATH = r'C:\Temp\Pdf2Txt\Comdirect'


FILE_LIST = []

def SearchFilesInPath(rootPath):
    ret_File_List = []
    for root, directories, filenames in os.walk(rootPath):
        for directory in directories:
            print(os.path.join(root, directory))
        for filename in filenames:
            filePath = os.path.join(root, filename)
            # print(filePath)
            ret_File_List.append(filePath)
    return ret_File_List


def pdf2TextConvertor(pdfInFile, DestDir = ""):
    print("processing file: {fName}".format(fName=pdfInFile))
    # with pdfplumber.open(inFile) as pdf:
    #     pages = pdf.pages
    #     for i,pg in enumerate(pages[:-1]):
    #         print(pg)
    #         tbl = pages[i].extract_tables()
    #         print(f'{i} --- {tbl}')
    #         text = pages[i].extract_text()
    #         print(text)
    folderPath, fileName = os.path.split(pdfInFile)
    fileName = os.path.splitext(fileName)[0]
    folderName = os.path.basename(folderPath)
    tmpPath = ""
    if DestDir == "":
        tmpPath = os.path.join(TEMP_PATH, "Kontoauszuege")
    else:
        tmpPath = os.path.join(DestDir, "Kontoauszuege")
    if folderName.isdigit():
        tmpPath = os.path.join(tmpPath, folderName)
    if not os.path.exists(tmpPath):
        os.makedirs(tmpPath)
    outputFile = os.path.join(tmpPath, fileName + ".txt")
    # if os.path.exists(outputFile):
    #     outputFile = os.path.join(tmpPath, fileName + "_1.txt")

    args = ["pdf2txt",  # actual value doesn't matter
            "-dNOPAUSE",
            "-sDEVICE=txtwrite",
            "-sOutputFile=" +outputFile,
            pdfInFile]
    # with ghostscript.Ghostscript(*args) as gs:
    #     gs.exit()
    encoding = locale.getpreferredencoding()
    args = [a.encode(encoding) for a in args]
    with ghostscript.Ghostscript(*args) as gs:
        print("Done!")
        ghostscript.cleanup()
    # try:
    #     GS = ghostscript.Ghostscript(*args)
    # except:
    #     GS.exit()
    # finally:
    #     GS.exit()
    return outputFile

def textFileProc(inTextFile):
    lines= []
    lines2Write =[]
    ENTRY_DETECTED = False
    entryDate = ""
    entryText = ""
    entryValue = ""
    fileDate = ""
    with open(inTextFile) as f:
        lines = f.readlines()
    for line in lines:
        # preparedLine = []
        lineElement = line.strip().split(" ")
        if lineElement[0] == "Datum" and checkDate(lineElement[-1]):
            fileDate = lineElement[-1]
        # if lineElement[0].count(".") == 2 and checkNumeric(lineElement[-1]):
        if checkDate(lineElement[0].strip()) and checkNumeric(lineElement[-1]):
            '''
            New entry detected
            todo: check Date
            '''
            print(lineElement)
            if entryDate != "":
                # in case entry has no line "Referenz:"
                if "-" in entryValue:
                    lines2Write.append([entryDate, entryText, entryValue])
                else:
                    lines2Write.append([entryDate, entryText, "",entryValue])
            ENTRY_DETECTED = True
            entryDate = lineElement[0].strip()
            entryValue = lineElement[-1].strip()
            entryText = line.replace(entryDate, "").replace(entryValue, "").strip()
        elif line.strip().startswith("Referenz:") and ENTRY_DETECTED == True:
            entryText += ("++" + line.strip())
            if "-" in entryValue:
                lines2Write.append([entryDate, entryText, entryValue])
            else:
                lines2Write.append([entryDate, entryText, "",entryValue])
            entryDate = ""
            entryText = ""
            entryValue = ""
            ENTRY_DETECTED = False
        elif ENTRY_DETECTED == True and checkEntryContent(line):
            entryText += ("++" + line.replace(entryDate, "").strip())
        elif "Alter Saldo" in line:
            lines2Write.append(["Alter Saldo","","","",lineElement[-2].strip()])
            entryDate = ""
            entryText = ""
            entryValue = ""
        elif "Neuer Saldo" in line and "Alter Saldo" != lines2Write[-1][0]:
            '''
            the line "Neuer Saldo" at the beginning of the statement should be ignored
            '''
            lines2Write.append(["Neuer Saldo",fileDate ,"","",lineElement[-1].strip()])
            entryDate = ""
            entryText = ""
            entryValue = ""
    return lines2Write
    # with open(os.path.join(TEMP_PATH,"output.csv"), "w", newline='') as f:
    #     writer = csv.writer(f, delimiter=';')
    #     writer.writerows(lines2Write)
        

def checkNumeric(inString):
    str = inString.replace(",","").replace("-", "").strip()
    try:
        float(str)
        return True
    except:
        return False

def checkDate(inString, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        if inString.count(".") == 2:
            parse(inString, fuzzy=fuzzy)
            return True
        else:
            return False
    except ValueError:
        return False


def checkEntryContent(inLine):
    inLineSplit = inLine.strip().split(" ")
    whiteSpaceCnt = (len(inLine) - len(inLine.lstrip(' ')))
    if not checkNumeric(inLineSplit[-1]) and (whiteSpaceCnt == 31 or
                                         checkDate(inLineSplit[0].strip())):
        return True
    else:
        return False

if __name__ == "__main__":
    FILE_LIST = SearchFilesInPath(ROOT_PATH)
    CSV_CONTENT = [["Date", "Text", "Expense", "Income", "Balance"]]
    for file in FILE_LIST:
       textFile = pdf2TextConvertor(file)
       CSV_CONTENT.extend(textFileProc(textFile))
    # textFileProc(pdf2TextConvertor(FILE_LIST[0]))
    with open(os.path.join(TEMP_PATH,"output.csv"), "w", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(CSV_CONTENT)
