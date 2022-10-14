class Biobank():
    """
    This class describes the biobank class
    """
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

        :param parent_url: Parent's catalog URL of a biobank. NOTE this url should exist in an FDP
        :param publisher_url: URL of the publisher of a biobank
        :param title: Title of a biobank
        :param description: Description of a biobank
        :param populationcoverage: Description of the coverage of a biobank
        :param themes: Themes URLs to describe a biobank
        :param publisher_name: Name of publisher of a biobank
        :param pages: Landing page URLs of a biobank
        """
        self.PARENT_URL = parent_url
        self.PUBLISHER_URL = publisher_url
        self.TITLE = title
        self.DESCRIPTION = description
        self.POPULATIONCOVERAGE = populationcoverage
        self.THEMES = themes
        self.PUBLISHER_NAME = publisher_name
        self.LANDING_PAGES = pages