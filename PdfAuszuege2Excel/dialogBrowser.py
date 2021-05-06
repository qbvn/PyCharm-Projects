import PySimpleGUI as sg
import os

#help(sg.FolderBrowse)
#help(sg.FileBrowse)


def getDirectories():
    inputDir = ""
    outputDir = ""

    layout = [
    [sg.Text("Input folder\t"), sg.Input(key='_IN_'), sg.FolderBrowse('Browse')],
    [sg.Text("Output folder\t"), sg.Input(key='_OUT_'), sg.FolderBrowse('Browse')],
    [sg.Submit('Process'), sg.Cancel()],
    ]

    window = sg.Window('PDF ING-Auszuege -> Excel-Report', layout)

    while True:
        event, values = window.read()
        #print('event:', event)
        #print('values:', values)
        # print('FolderBrowse:', values['FolderBrowse'])
        # print('FileBrowse:', values['FileBrowse'])
        
        inputDir = values.get('_IN_', "")
        outputDir = values.get('_OUT_', "")

        if event is None or event == 'Cancel':
            inputDir = ""
            outputDir = ""
            break
        elif event == "Process":
            break
        
        # if event == 'Submit':
        #     # if folder was not selected then use current folder `.`
        #     foldername = values['FolderBrowse'] or '.' 

        #     filenames = os.listdir(foldername)
            
        #     print('folder:', foldername)
        #     print('files:', filenames)
        #     print("\n".join(filenames))
    window.close()
    return inputDir, outputDir
if __name__ == "__main__":
    print(getDirectories())