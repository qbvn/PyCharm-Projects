from datetime import datetime
import re


class StimulusProfile:
    def __init__(self, root_tree):
        """
        This class grabs and saves all stimulus profile manager information from the NI XML file
        :param root_tree:
        """
        self.path = ""
        self.name = ""
        self.description = ""

        Reference_tree = root_tree.findall('References')[0]
        Reference_tree = Reference_tree.findall('Reference')[0]
        self.name = Reference_tree.attrib["name"]
        self.path = Reference_tree.iter("{urn:IEEE-1671:2010:Common}Text").next().text
        Testdescription_tree = root_tree.findall('TestDescription')[0]

        try:
            self.description = Testdescription_tree.iter('{urn:IEEE-1671:2010:Common}Description').next().text
        except:
            self.description = ""

class Testrun:
    def __init__(self, testrun_elementtree):
        """
        This class grabs and saves all testrun information from the NI XML file
        :param testrun_elementtree:
        """
        self.path = ""
        self.name = ""
        self.starttime = 0
        self.endtime = 0
        self.runningTime_seconds = 0
        self.result = ""
        self.timedelta = ""
        self.path = testrun_elementtree.iter("{urn:IEEE-1671:2010:Common}Text").next().text
        self.name = testrun_elementtree.attrib["name"]
        self.starttime = testrun_elementtree.attrib["startDateTime"]
        self.endtime = testrun_elementtree.attrib["endDateTime"]

        self.starttime = self.createDateTime(self.starttime)
        self.endtime = self.createDateTime(self.endtime)

        self.timedelta = self.endtime - self.starttime
        self.clalcRunningTime()
        self.result = testrun_elementtree.iter("Outcome").next().attrib["value"]

        try:
            Testdescription_tree = testrun_elementtree.findall('Description')[0]
            self.description = Testdescription_tree.text
        except:
            self.description = ""


    def clalcRunningTime(self):
        """
        calculates the testrun running time
        """
        self.runningTime_seconds = self.timedelta.total_seconds()

    def createDateTime(self, xml_date):
        """
        converts the raw date information from ni xml file to a datetime object
        :type xml_date: string
        """
        re_matches = re.match("^(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)", xml_date)

        year, month, day, hour, minute, seconds = re_matches.groups()

        return datetime(*map(int, [year, month, day, hour, minute, seconds]))

class ErrorElements:
    def __init__(self,Elementtree):

        self.name = ""
        self.ID = ""
        self.ErrorDescription = ""
        self.parse_error_element(Elementtree)


    def parse_error_element(self,Elementtree):
        self.name = Elementtree.attrib["name"]
        self.ID = Elementtree.attrib["ID"]
        self.ErrorDescription = Elementtree.findall('Outcome')[0].attrib["qualifier"]




