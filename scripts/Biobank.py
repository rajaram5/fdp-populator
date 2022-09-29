class Biobank():
    """
    This class describes the biobank class
    """
    PARENT_URL = None
    TITLE = None
    DESCRIPTION = None
    POPULATIONCOVERAGE = None
    THEMES = []
    PUBLISHER = None
    LANDING_PAGES = None


    def __init__(self, parent_url, title, description, populationcoverage, themes, publisher, pages):
        """

        :param parent_url: Parent's catalog URL of a biobank. NOTE this url should exist in an FDP
        :param title: Title of a biobank
        :param description: Description of a biobank
        :param populationcoverage: Description of the coverage of a biobank
        :param themes: Themes URLs to describe a biobank
        :param publisher: Publisher URL of a biobank (e.g. https://orcid.org/0000-0002-1215-167X)
        :param pages: Landing page URLs of a biobank
        """
        self.PARENT_URL = parent_url
        self.TITLE = title
        self.DESCRIPTION = description
        self.POPULATIONCOVERAGE = populationcoverage
        self.THEMES = themes
        self.PUBLISHER = publisher
        self.LANDING_PAGES = pages