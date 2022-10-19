import chevron
from rdflib import Graph

class VPResource:
    """
    Super class contents generic resource metadata properties
    """
    PARENT_URL = None
    TITLE = None
    DESCRIPTION = None
    PUBLISHER_URL = None
    LICENSE_URL = None
    VERSION = None

    def __init__(self, parent_url, title, description, publisher, license, version):
        """
        :param parent_url: Parent's FDP URL of a resource
        :param title: Title of a resource
        :param description: Description of a resource
        :param publisher: Publisher URL of a resource (e.g. https://orcid.org/0000-0002-1215-167X)
        :param language: Language URL of a resource (e.g. http://id.loc.gov/vocabulary/iso639-1/en)
        :param license: License URL of a resource (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0)
        """
        self.PARENT_URL = parent_url
        self.TITLE = title
        self.DESCRIPTION = description
        self.PUBLISHER_URL = publisher
        self.LICENSE_URL = license
        self.VERSION = version

    def get_graph(self):
        graph = Graph()

        with open('../templates/vpresource.mustache', 'r') as f:
            body = chevron.render(f, {'parent_url': self.PARENT_URL, 'title': self.TITLE,
                                      'description': self.DESCRIPTION, 'publisher_url': self.PUBLISHER_URL,
                                      'license_url': self.LICENSE_URL, 'version': self.VERSION})
            print("VPResource class output:")
            print("publisher:", self.PUBLISHER_URL)
            print(body)
            graph.parse(data=body, format="turtle")

        return(graph)
