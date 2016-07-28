from distutils.core import setup
import py2exe

#setup(options = {
#        "py2exe": {
#            "dll_excludes": ["MSVCP90.dll"]
#        }
#    }, console=['main.py'])

setup(
	windows = [{'script': 'main.py'}],
    options = {
        "py2exe" : {
		            #'compressed': 1,
                    'optimize': 2,
                    #'includes': includes,
                    #'excludes': excludes,
                    #'packages': packages,
                    #'dll_excludes': dll_excludes,
                    'bundle_files': 1,  # 1 = .exe; 2 = .zip; 3 = separate

            "includes" : [	'sys','os', 'PySide.QtGui','PySide.QtCore','docx',
							'lxml.etree', 'lxml._elementpath',
							'XmlAnalysis', 'XmlParser', 'NiXml' ],
			"dll_excludes": ["MSVCP90.dll"]
					}
				}#,zipfile=None,
				#, console =['main.py']
				)