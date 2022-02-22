import Resource


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