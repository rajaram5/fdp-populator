import chevron
from rdflib import Graph

class VPResource:
    """
    Super class contents generic resource metadata properties
    """
    URL = None
    PARENT_URL = None
    TITLE = None
    DESCRIPTION = None
    PUBLISHER_URL = None
    PUBLISHER_NAME = None
    LICENSE_URL = None
    VERSION = None

    def __init__(self, parent_url, title, description, publisher_url, publisher_name, license, version, access, access_type):
        """
        :param parent_url: Parent's FDP URL of a resource
        :param title: Title of a resource
        :param description: Description of a resource
        :param publisher_url: Publisher URL of a resource (e.g. https://orcid.org/0000-0002-1215-167X)
        :param publisher_name: Publisher name of a resource
        :param language: Language URL of a resource (e.g. http://id.loc.gov/vocabulary/iso639-1/en)
        :param license: License URL of a resource (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0)
        """
        self.PARENT_URL = parent_url
        self.TITLE = title
        self.DESCRIPTION = description
        self.PUBLISHER_URL = publisher_url
        self.PUBLISHER_NAME = publisher_name
        self.LICENSE_URL = license
        self.VERSION = version
        self.ACCESS = access
        self.ACCESS_TYPE = access_type

    def get_graph(self):
        graph = Graph()

        if self.ACCESS_TYPE == "Access Information":
            self.ACCESS_TYPE = "dct:accessRight"
        elif self.ACCESS_TYPE == "ODRL Policy":
            self.ACCESS_TYPE = "odrl:hasPolicy"
        else:
            print("Unexcepted access type: ", self.ACCESS_TYPE, ", defaulting to no access information")
            self.ACCESS = ""

        with open('../templates/vpresource.mustache', 'r') as f:
            body = chevron.render(f, {'parent_url': self.PARENT_URL, 'title': self.TITLE,
                                      'description': self.DESCRIPTION, 'publisher_url': self.PUBLISHER_URL,
                                      'license_url': self.LICENSE_URL, 'version': self.VERSION,
                                      'access': self.ACCESS, 'access_type': self.ACCESS_TYPE})
            graph.parse(data=body, format="turtle")

        return(graph)
