import Resource

class Distribution(Resource.Resource):
    """
    This class extends Resource class with distribution specific properties
    """
    ACCESS_URL = None
    DOWNLOAD_URL = None
    MEDIA_TYPE = None
    COMPRESSION_FORMAT = None
    FORMAT = None
    BYTE_SIZE = None
    DATASET_NAME = None

    def __init__(self, parent_url, title, description, publisher, language, license,
                 access_url, download_url, media_type, compression_format, format,
                 byte_size, dataset_name):
        """
        
        :param parent_url: Dataset URL of a distribution. NOTE: this url should exist in an FDP
        :param title: Title of a distribution
        :param description: Description of a distribution
        :param publisher: Publisher URL of a distribution (e.g. https://orcid.org/0000-0002-1215-167X)
        :param language: Language URL of a distribution (e.g. http://id.loc.gov/vocabulary/iso639-1/en)
        :param license: License URL of a distribution (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0)
        :param access_url: Access URL of a distribution
        :param download_url: Download URL of a distribution
        :param media_type: Mediatype of a distribution (e.g. text/turtle)
        :param compression_format: compress format of a distribution
        :param format: Format of a distribution (e.g. application/gzip)
        :param byte_size: Byte size of a distribution (e.g. 987978)
        :param dataset_name: Dataset name of a distribution
        """
        # Pass core properties to parent class
        super().__init__(parent_url, title, description, publisher, language, license)
        self.ACCESS_URL = access_url
        self.DOWNLOAD_URL = download_url
        self.MEDIA_TYPE = media_type
        self.COMPRESSION_FORMAT = compression_format
        self.FORMAT = format
        self.BYTE_SIZE = byte_size
        self.DATASET_NAME = dataset_name