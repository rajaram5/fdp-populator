import Utils
import chevron
from rdflib import Graph
from resource_classes import VPResource

class VPDataService(VPResource.VPResource):
    """
    This class extends Resource class with properties specific to dataset properties
    """
    ENDPOINT_URL = None
    DATASET_NAMES = []
    DATASET_URLS = []
    CONFORMS_TO = None


    def __init__(self, parent_url, title, description, publisher_url, publisher_name, license, version, endpoint_url, serves_dataset_names, serves_dataset_urls, conforms_to, access, access_type):
        """

        :param parent_url: Parent's FDP URL of a resource
        :param title: Title of a resource
        :param description: Description of a resource
        :param publisher_url: Publisher URL of a resource (e.g. https://orcid.org/0000-0002-1215-167X)
        :param publisher_name: Publisher name of a resource
        :param language: Language URL of a resource (e.g. http://id.loc.gov/vocabulary/iso639-1/en)
        :param license: License URL of a resource (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0)
        :param endpoint_url: Url of the endpoint
        :param serves_dataset_names: Names of the datasets the dataservice serves
        :param serves_dataset_urls: URLs of the datasets the dataservice serves
        :param conforms to: specification the dataservice conforms to TODO: double check
        """
        # Pass core properties to parent class
        super().__init__(parent_url, title, description, publisher_url, publisher_name, license, version, access, access_type)

        self.ENDPOINT_URL = endpoint_url
        self.DATASET_NAMES = serves_dataset_names
        self.DATASET_URLS = serves_dataset_urls
        self.CONFORMS_TO = conforms_to
    
    def get_graph(self):
        """
        Method to get dataservice RDF

        :return: dataservice RDF
        """
        utils = Utils.Utils()
        graph = super().get_graph()

        serves_datasets_str = utils.list_to_rdf_URIs(self.DATASET_URLS)

        with open('../templates/vpdataservice.mustache', 'r') as f:
            body = chevron.render(f, {'endpoint_url': self.ENDPOINT_URL, 'dataset_urls': serves_datasets_str,
                                      'conforms_to': self.CONFORMS_TO})
            graph.parse(data=body, format="turtle")

        return graph