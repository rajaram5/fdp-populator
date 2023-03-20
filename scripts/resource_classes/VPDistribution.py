import Utils
import chevron
from rdflib import Graph
from resource_classes import VPResource

class VPDistribution(VPResource.VPResource):
    """
    This class extends Resource class with properties specific to dataset properties
    """

    DATASET_TITLE = None
    URL = None
    URL_TYPE = None
    MEDIATYPE = None
    ISPARTOF = []


    def __init__(self, parent_url, title, dataset_title, description, publisher_url, publisher_name, license, version, url, url_type, mediatype, ispartof, access, access_type):
        """

        :param parent_url: Parent's catalog URL of a dataset. NOTE this url should exist in an FDP
        :param title: Title of a dataset
        :param description: Description of a dataset
        :param publisher_url: Publisher URL of a resource (e.g. https://orcid.org/0000-0002-1215-167X)
        :param publisher_name: Publisher name of a resource
        :param license: License URL of a resource (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0)
        :param version
        :param url
        :param url_type
        :param mediatype
        :param ispartof
        """
        # Pass core properties to parent class
        super().__init__(parent_url, title, description, publisher_url, publisher_name, license, version, access, access_type)

        self.DATASET_TITLE = dataset_title
        self.URL = url
        self.URL_TYPE = url_type
        self.MEDIATYPE = mediatype
        self.ISPARTOF = ispartof

    
    def get_graph(self):
        """
        Method to get dataset RDF

        :return: dataset RDF
        """
        utils = Utils.Utils()
        graph = super().get_graph()

        ispartof_str = utils.list_to_rdf_URIs(self.ISPARTOF)
        is_downloadurl = self.URL_TYPE == 'Download'
        is_accessurl = self.URL_TYPE == 'Access'

        with open('../templates/vpdistribution.mustache', 'r') as f:
            body = chevron.render(f, {'url': self.URL, 'is_downloadurl': is_downloadurl,
                                    'is_accessurl': is_accessurl, 'mediatype': self.MEDIATYPE,
                                    'ispartof': ispartof_str})
            graph.parse(data=body, format="turtle")

        return graph
    