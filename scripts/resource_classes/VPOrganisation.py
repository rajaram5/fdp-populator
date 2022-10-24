import chevron
from rdflib import Graph

class VPOrganisation():
    """
    This class describes the organisation class
    """
    URL = None
    PARENT_URL = None
    TITLE = None
    DESCRIPTION = None
    LOCATION_TITLE = None
    LOCATION_DESCRIPTION = None
    LANDING_PAGES = None


    def __init__(self, parent_url, title, description, location_title, location_description, pages):
        """

        :param parent_url: Parent's catalog URL of an organisation. NOTE this url should exist in an FDP
        :param title: Title of an organisation
        :param description: Description of an organisation
        :param location_title: title of a location of an organisation
        :param location_title: description of a location of an organisation
        :param pages: Landing page URLs of an organisation
        """
        self.PARENT_URL = parent_url
        self.TITLE = title
        self.DESCRIPTION = description
        self.LOCATION_TITLE = location_title
        self.LOCATION_DESCRIPTION = location_description
        self.LANDING_PAGES = pages
    
    def get_graph(self):
        """
        Method to get organisation RDF

        :return: organisation RDF
        """
        # Create pages list
        page_str = ""
        for page in self.LANDING_PAGES:
            page_str = page_str + " <" + page + ">,"
        page_str = page_str[:-1]

        # Render RDF
        graph = Graph()

        with open('../templates/vporganisation.mustache', 'r') as f:
            body = chevron.render(f, {'parent_url': self.PARENT_URL,
                                      'title': self.TITLE,
                                      'description': self.DESCRIPTION,
                                      'location_title': self.LOCATION_TITLE,
                                      'location_description': self.LOCATION_DESCRIPTION,
                                      'pages': page_str})
            graph.parse(data=body, format="turtle")

        return graph