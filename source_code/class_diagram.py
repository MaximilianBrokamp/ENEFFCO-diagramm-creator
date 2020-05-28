#class to save all aspekts related to a specific diagram

class diagram:

    def __init__(self):
        self.diagram_name = ""
        self.template_file = ""
        self.template_path = ""
        #self.hierarchical_codes = hierarchical_codes
        self.plants_with_created_diagram = []
        self.diagram_type = ""
        self.report_name = ""
        self.ignore_list = []
        self.select_list = []
        self.config_file_name = ""
    def set_diagram_name(self, diagram_name):
        self.diagram_name = diagram_name
    def add_plant(self, data):
        self.plants_with_created_diagram.append(data)
    def set_type(self, diagram_type):
        self.diagram_type = diagram_type
    def set_ignore(self, ignore_list):
        self.ignore_list = ignore_list
    def set_select(self, select_list):
        self.select_list = select_list
    def set_report_name(self, report_name):
        self.report_name = report_name
