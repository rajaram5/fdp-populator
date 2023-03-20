import FDPClient
import Config
import Utils
from template_readers import FDPTemplateReader, VPTemplateReader
import uuid



class Populator:
    """
    Class contents methods to extract content from the input CSV files and methods to populate FDP with content.
    """
    FDP_CLIENT = FDPClient.FDPClient(Config.FDP_URL, Config.FDP_USERNAME, Config.FDP_PASSWORD,
                                     Config.FDP_PERSISTENT_URL)
    UTILS = Utils.Utils()

    def __init__(self):
        """
        This __init__ method exacts datasets and distribution objects from the input CSV files. These objects are used to
        create metadata entries in the FAIR Data Point.
        """

        # Read FDP templates and write to FDP if configured to do this
        if Config.DATASET_INPUT_FILE != None and Config.DISTRIBUTION_INPUT_FILE != None:
            # Get dataset and distribution data
            fdp_template_reader = FDPTemplateReader.FDPTemplateReader()
            datasets = fdp_template_reader.get_datasets()
            distributions = fdp_template_reader.get_distributions()

            # Populate FDP with datasets
            for dataset_name, dataset in datasets.items():
                dataset_url = self.create_resource(dataset, "dataset")
                # Populate FDP with distribution(s) as child to dataset
                for distribution_name, distribution in distributions.items():
                    if distribution.DATASET_NAME == dataset_name:
                        distribution.PARENT_URL = dataset_url

                        # This logic is required since both download and access URLs are captured in same row
                        download_url = distribution.DOWNLOAD_URL
                        distribution_name = distribution.TITLE
                        if distribution.ACCESS_URL:
                            distribution.TITLE = "Access distribution of : " + distribution_name
                            distribution.DOWNLOAD_URL = None
                            self.create_resource(distribution, "distribution")

                        if download_url:
                            distribution.TITLE = "Downloadable distribution of : " + distribution_name
                            distribution.ACCESS_URL = None
                            distribution.DOWNLOAD_URL = download_url
                            self.create_resource(distribution, "distribution")

        # Read VP templates and write to FDP if configured to do this
        if Config.EJP_VP_INPUT_FILE != None:
            # Read the excel template
            vp_template_reader = VPTemplateReader.VPTemplateReader()
            organisations = vp_template_reader.get_organisations()
            biobanks = vp_template_reader.get_biobanks()
            patientregistries = vp_template_reader.get_patientregistries()
            datasets = vp_template_reader.get_datasets()
            distributions = vp_template_reader.get_distributions()
            dataservices = vp_template_reader.get_dataservices()

            # Create organisation entries first
            for organisation_name, organisation in organisations.items():
                organisation.URL = self.create_resource(organisation, "organisation")

            # Create biobank entries
            for biobank_name, biobank in biobanks.items():
                # Link organisation
                for organisation_name, organisation in organisations.items():
                    if biobank.PUBLISHER_NAME == organisation.TITLE:
                        biobank.PUBLISHER_URL = organisation.URL
                
                # Create entry
                biobank.URL = self.create_resource(biobank, "biobank")

            # Create patient registry entries
            for patientregistry_name, patientregistry in patientregistries.items():
                # Link organisation
                for organisation_name, organisation in organisations.items():
                    if patientregistry.PUBLISHER_NAME == organisation.TITLE:
                        patientregistry.PUBLISHER_URL = organisation.URL

                # Create entry
                patientregistry.URL = self.create_resource(patientregistry, "patientregistry")

            # Create datasets
            for dataset_name, dataset in datasets.items():
                # Link organisation
                for organisation_name, organisation in organisations.items():
                    if dataset.PUBLISHER_NAME == organisation.TITLE:
                        dataset.PUBLISHER_URL = organisation.URL

                # Create entry
                dataset.URL = self.create_resource(dataset, "dataset")

            # Create distributions
            for distribution_name, distribution in distributions.items():
                # Link organisation
                for organisation_name, organisation in organisations.items():
                    if distribution.PUBLISHER_NAME == organisation.TITLE:
                        distribution.PUBLISHER_URL = organisation.URL

                # Link dataset
                for dataset_name, dataset in datasets.items():
                    if distribution.DATASET_TITLE == dataset.TITLE:
                        distribution.PARENT_URL = dataset.URL

                # Create entry
                distribution.URL = self.create_resource(distribution, "distribution")

            # Create dataservices
            for dataservice_name, dataservice in dataservices.items():
                # Link datasets
                for dataset_name, dataset in datasets.items():
                    if dataset.TITLE in dataservice.DATASET_NAMES:
                        dataservice.DATASET_URLS.append(dataset.URL)

                # Link organisation
                for organisation_name, organisation in organisations.items():
                    if dataservice.PUBLISHER_NAME == organisation.TITLE:
                        dataservice.PUBLISHER_URL = organisation.URL

                # Create entry
                dataservice.URL = self.create_resource(dataservice, "dataservice")

    def create_resource(self, resource, resource_type):
        """
        Method to create resource of resource type in FDP

        :param dataset: Provide resource object
        :param resource_type: Provide the type of resource
        :return: FDP's dataset URL
        """
        # Check if parent exists
        parent_url = resource.PARENT_URL

        if not Config.DRY_RUN and not self.FDP_CLIENT.does_metadata_exists(parent_url):
            raise SystemExit("The parent metadata <"+parent_url+"> does not exist. Provide valid catalog URL")

        print("The catalog <"+parent_url+"> exist")

        # Obtain graph that should be sent to FDP
        graph = resource.get_graph()

        # Serialize graph and send to FDP
        post_body = graph.serialize(format='turtle')
        print("Sending the following RDF to FDP:")
        print(post_body)
        if Config.DRY_RUN:
            resource_url = "http://example.org/" + resource_type + "/" + str(uuid.uuid4())
        else:
            resource_url = self.FDP_CLIENT.fdp_create_metadata(post_body, resource_type)
        print("New " + resource_type + " created: " + resource_url)
        return resource_url