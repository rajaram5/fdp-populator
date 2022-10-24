import chevron
from rdflib import Graph

class VPPatientregistry():
    """
    This class describes the patient registry class
    """
    URL = None
    PARENT_URL = None
    PUBLISHER_URL = None
    TITLE = None
    DESCRIPTION = None
    POPULATIONCOVERAGE = None
    THEMES = []
    PUBLISHER_NAME = None
    LANDING_PAGES = None


    def __init__(self, parent_url, publisher_url, title, description, populationcoverage, themes, publisher_name, pages):
        """

        :param parent_url: Parent's catalog URL of a patient registry. NOTE this url should exist in an FDP
        :param publisher_url: URL of the publisher of a patient registry
        :param title: Title of a patient registry
        :param description: Description of a patient registry
        :param populationcoverage: Description of the coverage of a patient registry
        :param themes: Themes URLs to describe a patient registry
        :param publisher_name: Name of publisher of a patient registry
        :param pages: Landing page URLs of a patient registry
        """
        self.PARENT_URL = parent_url
        self.PUBLISHER_URL = publisher_url
        self.TITLE = title
        self.DESCRIPTION = description
        self.POPULATIONCOVERAGE = populationcoverage
        self.THEMES = themes
        self.PUBLISHER_NAME = publisher_name
        self.LANDING_PAGES = pages

    def get_graph(self):
        """
        Method to get patient registry RDF

        :return: patient registry RDF
        """
        # Create themes list
        theme_str = ""
        for theme in self.THEMES:
            theme_str = theme_str + " <" + theme + ">,"
        theme_str = theme_str[:-1]

        # Create pages list
        page_str = ""
        for page in self.LANDING_PAGES:
            page_str = page_str + " <" + page + ">,"
        page_str = page_str[:-1]

        # Render RDF
        graph = Graph()

        with open('../templates/vppatientregistry.mustache', 'r') as f:
            body = chevron.render(f, {'parent_url': self.PARENT_URL,
                                      'title': self.TITLE,
                                      'description': self.DESCRIPTION,
                                      'populationcoverage': self.POPULATIONCOVERAGE,
                                      'themes': theme_str,
                                      'publisher': self.PUBLISHER_URL,
                                      'pages': page_str})
            graph.parse(data=body, format="turtle")

        return graph
