from resource_classes import Resource
import Utils
import chevron
from rdflib import Graph

class Dataset(Resource.Resource):
    """
    This class extends Resource class with properties specific to dataset properties
    """
    KEYWORDS = []
    THEMES = []
    LANDING_PAGE = None
    CONTACT_POINT = None


    def __init__(self, parent_url, title, description, keywords, themes, publisher, language,
                 license, page, contact_point):
        """

        :param parent_url: Parent's catalog URL of a dataset. NOTE this url should exist in an FDP
        :param title: Title of a dataset
        :param description: Description of a dataset
        :param keywords: Keywords to describe a dataset
        :param themes: Themes URLs to describe a dataset
        :param publisher: Publisher URL of a dataset (e.g. https://orcid.org/0000-0002-1215-167X)
        :param language: Language URL of a dataset (e.g. http://id.loc.gov/vocabulary/iso639-1/en)
        :param license: License URL of a resource (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0)
        :param page: Landing page URL of a dataset
        :param contact_point: Contact point URL or mailto URL of a dataset
        """
        # Pass core properties to parent class
        super().__init__(parent_url, title, description, publisher, language, license)
        self.KEYWORDS = keywords
        self.THEMES = themes
        self.LANDING_PAGE = page
        self.CONTACT_POINT = contact_point
    
    def get_graph(self):
        """
        Method to get dataset RDF

        :return: dataset RDF
        """
        self.UTILS = Utils.Utils()
        graph = Graph()

        # create resource triples
        self.UTILS.add_resource_triples(self, graph)
        # Create language triples
        self.UTILS.add_language_triples(self, graph)
        # Create license triples
        self.UTILS.add_licence_triples(self, graph)

        # Create landing page triples
        if self.LANDING_PAGE:
            with open('../templates/landingpage.mustache', 'r') as f:
                body = chevron.render(f, {'page_url': self.LANDING_PAGE})
                graph.parse(data=body, format="turtle")

        # Create contact point triples
        if self.CONTACT_POINT:
            with open('../templates/contact.mustache', 'r') as f:
                body = chevron.render(f, {'contact_url': self.CONTACT_POINT})
                graph.parse(data=body, format="turtle")

        # Create keywords list
        keyword_str = ""
        for keyword in self.KEYWORDS:
            keyword_str = keyword_str + ' "' + keyword + '",'
        keyword_str = keyword_str[:-1]

        # Create themes list
        theme_str = ""
        for theme in self.THEMES:
            theme_str = theme_str + " <" + theme + ">,"
        theme_str = theme_str[:-1]

        # create dataset triples
        with open('../templates/dataset.mustache', 'r') as f:
            body = chevron.render(f, {'keyword': keyword_str, 'theme': theme_str})
            graph.parse(data=body, format="turtle")

        return graph