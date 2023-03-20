import Utils
import chevron
from rdflib import Graph
from resource_classes import VPResource

class VPDataset(VPResource.VPResource):
    """
    This class extends Resource class with properties specific to dataset properties
    """
    LANGUAGE_URL = None
    KEYWORDS = []
    THEMES = []
    LANDING_PAGE = None
    CONTACT_POINT = None
    KEYWORDS = []
    THEMES = []
    LANDING_PAGE = None
    CONTACT_POINT = None


    def __init__(self, parent_url, title, description, keywords, themes, publisher_url, publisher_name,
                 language, license, page, contact_point, vpconnection, related, version, access, access_type):
        """

        :param parent_url: Parent's catalog URL of a dataset. NOTE this url should exist in an FDP
        :param title: Title of a dataset
        :param description: Description of a dataset
        :param keywords: Keywords to describe a dataset
        :param themes: Themes URLs to describe a dataset
        :param publisher_url: Publisher URL of a resource (e.g. https://orcid.org/0000-0002-1215-167X)
        :param publisher_name: Publisher name of a resource
        :param language: Language URL of a dataset (e.g. http://id.loc.gov/vocabulary/iso639-1/en)
        :param license: License URL of a resource (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0)
        :param page: Landing page URL of a dataset
        :param contact_point: Contact point URL or mailto URL of a dataset
        :param vpconnection
        :param related
        :param version
        """
        # Pass core properties to parent class
        super().__init__(parent_url, title, description, publisher_url, publisher_name, license, version, access, access_type)

        self.KEYWORDS = keywords
        self.THEMES = themes
        self.LANGUAGE_URL = language
        self.LANDING_PAGE = page
        self.CONTACT_POINT = contact_point
        # TODO: Implement vpconnection and related after schema update
        self.VPCONNECTION = vpconnection
        self.RELATED = related
    
    def get_graph(self):
        """
        Method to get dataset RDF

        :return: dataset RDF
        """
        utils = Utils.Utils()
        graph = super().get_graph()

        self.THEMES.append(self.VPCONNECTION)

        theme_str = utils.list_to_rdf_URIs(self.THEMES)
        page_str = utils.list_to_rdf_URIs(self.LANDING_PAGE)
        keyword_str = utils.list_to_rdf_literals(self.KEYWORDS)

        with open('../templates/vpdataset.mustache', 'r') as f:
            body = chevron.render(f, {'theme': theme_str, 'page': page_str, 'keyword': keyword_str,
                                    'language': self.LANGUAGE_URL, 'contact_url': self.CONTACT_POINT})
            graph.parse(data=body, format="turtle")

        return graph