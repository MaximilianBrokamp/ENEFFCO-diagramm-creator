#class to save all aspekts related to a specific diagram

class diagram:

    def __init__(self, name=None, template_path=None, hierarchical_codes=None, special_datapoints=None):
        self.name = name
        self.template_path = template_path
        self.hierarchical_codes = hierarchical_codes
        self.special_datapoints = special_datapoints