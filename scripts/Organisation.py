class Organisation():
    """
    This class describes the organisation class
    """
    PARENT_URL = None
    TITLE = None
    DESCRIPTION = None
    LOCATION = None
    LANDING_PAGES = None


    def __init__(self, parent_url, title, description, location, pages):
        """

        :param parent_url: Parent's catalog URL of an organisation. NOTE this url should exist in an FDP
        :param title: Title of an organisation
        :param description: Description of an organisation
        :param location: location of an organisation
        :param pages: Landing page URLs of an organisation
        """
        self.PARENT_URL = parent_url
        self.TITLE = title
        self.DESCRIPTION = description
        self.LOCATION = location
        self.LANDING_PAGES = pages