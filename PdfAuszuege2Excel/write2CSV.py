import os as os
import csv
def writeLinesCSV(InputLinesList, DirPath, Filename):
    with open(os.path.join(DirPath, Filename + ".csv"), "w", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(InputLinesList)