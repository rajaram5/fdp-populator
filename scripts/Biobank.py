class Biobank():
    """
    This class describes the biobank class
    """
    PARENT_URL = None
    TITLE = None
    DESCRIPTION = None
    THEMES = []
    PUBLISHER = None
    LANDING_PAGE = None


    def __init__(self, parent_url, title, description, themes, publisher, page):
        """

        :param parent_url: Parent's catalog URL of a biobank. NOTE this url should exist in an FDP
        :param title: Title of a biobank
        :param description: Description of a biobank
        :param themes: Themes URLs to describe a biobank
        :param publisher: Publisher URL of a biobank (e.g. https://orcid.org/0000-0002-1215-167X)
        :param page: Landing page URL of a biobank
        """
        self.PARENT_URL = parent_url
        self.TITLE = title
        self.DESCRIPTION = description
        self.THEMES = themes
        self.PUBLISHER = publisher
        self.LANDING_PAGE = page