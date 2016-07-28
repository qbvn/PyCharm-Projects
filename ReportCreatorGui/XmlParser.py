import xml.etree.ElementTree as ET
from StringIO import StringIO
import re


class XmlParser:
    def __init__(self, xmlFile):

        """
        reads the file XML from NI Stimulus Profile Editor.
        Parse Elements from interest.

        :type xmlFile: path to xml file
        """
        self.xmlFile = xmlFile
        self.Testruns = []
        self.Reference_xml = ""
        self.elements_with_errors = []

        with open(self.xmlFile) as data:
            xml_text = data.read()

        # cleaning up the xml file for parsing
        xml_text = re.sub(' xmlns="[^"]+"', '', xml_text, count=1)

        tree = ET.parse(StringIO(xml_text))

        self.root = tree.getroot()
        self.parse_testrun()
        self.parse_errors()

    def parse_testrun(self):
        """
        parsing the xml file and grabs testrun elements
        :rtype: None
        """
        for TestCalls in self.root.iter('Test'):
            try:
                # print TestCalls.attrib["ID"]
                if "Call RealTimeSequence" in TestCalls.attrib["ID"]:
                    self.Testruns.append(TestCalls)
            except:
                pass  # no Sequence calls in File

    def parse_errors(self):

        # find all perante which store "Outcome" element
        parents = self.root.findall('.//Outcome/..')

        for parent in parents:

            for child in parent:

                try:
                    if "Error" in child.attrib["qualifier"]:
                        self.elements_with_errors.append(parent)
                except:
                    pass



    def parse_stimulus_profile(self):

        """
        parsing the xml file and grabs StimulusProfile information elements

        :rtype: None
        """
        self.Reference_xml = root.findall('References')[0]

    def get_error_elements(self):
        """

        :return:
        """
        return self.elements_with_errors

    def get_Simulus_profiles(self):
        """
        getter function
        :return: xml tree which stores stimulus profile information
        """
        return self.Reference_xml

    def get_testruns(self):
        """
        getter function

        :return: xml tree which stores the testrun information
        """
        return self.Testruns

    def get_root_tree(self):
        """
        getter function

        :return: xml root tree
        """

        return self.root


if __name__ == "__main__":
    xmlParser = XmlParser("Engine Demo Basics Test Result1.xml")

    for el in xmlParser.get_testruns():
        print(el)
