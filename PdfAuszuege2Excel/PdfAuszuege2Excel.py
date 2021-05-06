import dialogBrowser
import PdfProc
import write2CSV
import tempfile


if __name__ == "__main__":
    inputDir = ""
    outputDir = ""
    inputDir, outputDir = dialogBrowser.getDirectories()
    if inputDir == "" or outputDir == "":
        '''ToDo: Check path -> PopUp
        '''
        pass
    else:    

        '''Process content
        '''
        FILE_LIST = PdfProc.SearchFilesInPath(inputDir)
        CSV_CONTENT = [["Date", "Text", "Expense", "Income", "Balance"]]
        with tempfile.TemporaryDirectory() as tmpDir:
            print('created temporary directory', tmpDir)
            for file in FILE_LIST:
                textFile = PdfProc.pdf2TextConvertor(file, tmpDir)
                CSV_CONTENT.extend(PdfProc.textFileProc(textFile))

        '''write to file
        '''
        write2CSV.writeLinesCSV(CSV_CONTENT, outputDir, "ReportING" )
