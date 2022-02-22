class Resource:
    """
    Super class contents generic FDP metadata properties
    """
    PARENT_URL = None
    TITLE = None
    DESCRIPTION = None
    PUBLISHER_URL = None
    LANGUAGE_URL = None
    LICENSE_URL = None

    def __init__(self, parent_url, title, description, publisher, language, license):
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
        self.LANGUAGE_URL = language
        self.LICENSE_URL = license