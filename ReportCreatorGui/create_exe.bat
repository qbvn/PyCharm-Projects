::C:\Python27\Scripts\cxfreeze --include-modules=PySide.QtGui,PySide.QtCore,lxml,lxml.etree,lxml._elementpath --target-name=ReportCreator.exe main.py
::oder
::pip install pyinstaller==3.1.1
pyinstaller --onefile --windowed --icon=logo.ico main.py
