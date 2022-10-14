import FDPClient
import Config
import chevron
import Utils
import TemplateReader
from rdflib import Graph



class Populator:
    """
    Class contents methods to extract content from the input CSV files and methods to populate FDP with content.
    """
    FDP_CLIENT = FDPClient.FDPClient(Config.FDP_URL, Config.FDP_USERNAME, Config.FDP_PASSWORD,
                                     Config.FDP_PERSISTENT_URL)
    template_reader = TemplateReader.TemplateReader()
    UTILS = Utils.Utils()

    def __init__(self):
        """
        This __init__ method exacts datasets and distribution objects from the input CSV files. These objects are used to
        create metadata entries in the FAIR Data Point.
        """
        # GET datasets
        datasets = self.template_reader.get_datasets()
        # GET distributions
        distributions = self.template_reader.get_distributions()
        # Populate FDP with datasets
        for dataset_name, dataset in datasets.items():
            dataset_url = self.create_dataset(dataset)
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
                        self.create_distribution(distribution)

                    if download_url:
                        distribution.TITLE = "Downloadable distribution of : " + distribution_name
                        distribution.ACCESS_URL = None
                        distribution.DOWNLOAD_URL = download_url
                        self.create_distribution(distribution)

        # organisations = self.template_reader.get_organisations()
        # biobanks = self.template_reader.get_biobanks()
        # patientregistries = self.template_reader.get_patientregistries()

        # for organisation_name, organisation in organisations.items():
        #     organisation_url = self.create_organisation(organisation)
        #     for biobank_name, biobank in biobanks.items():
        #         if biobank.PUBLISHER_NAME == organisation.TITLE:
        #             biobank.PUBLISHER_URL = organisation_url
        #             self.create_biobank(biobank)
        #     for patientregistry_name, patientregistry in patientregistries.items():
        #         if patientregistry.PUBLISHER_NAME == organisation.TITLE:
        #             patientregistry.PUBLISHER_URL = organisation_url
        #             self.create_patientregistry(patientregistry)

    def create_dataset(self, dataset):
        """
        Method to create dataset in FDP

        :param dataset: Provide dataset object
        :return: FDP's dataset URL
        """
        parent_url = dataset.PARENT_URL

        if not self.FDP_CLIENT.does_metadata_exists(parent_url):
            raise SystemExit("The catalog <"+parent_url+"> doesn't exist. Provide valid catalog URL")

        print("The catalog <"+parent_url+"> exist")

        graph = Graph()

        # create resource triples
        self.UTILS.add_resource_triples(dataset, graph)
        # Create language triples
        self.UTILS.add_language_triples(dataset, graph)
        # Create license triples
        self.UTILS.add_licence_triples(dataset, graph)

        # Create landing page triples
        if dataset.LANDING_PAGE:
            with open('../templates/landingpage.mustache', 'r') as f:
                body = chevron.render(f, {'page_url': dataset.LANDING_PAGE})
                graph.parse(data=body, format="turtle")

        # Create contact point triples
        if dataset.CONTACT_POINT:
            with open('../templates/contact.mustache', 'r') as f:
                body = chevron.render(f, {'contact_url': dataset.CONTACT_POINT})
                graph.parse(data=body, format="turtle")

        # Create keywords list
        keyword_str = ""
        for keyword in dataset.KEYWORDS:
            keyword_str = keyword_str + ' "' + keyword + '",'
        keyword_str = keyword_str[:-1]

        # Create themes list
        theme_str = ""
        for theme in dataset.THEMES:
            theme_str = theme_str + " <" + theme + ">,"
        theme_str = theme_str[:-1]

        # create dataset triples
        with open('../templates/dataset.mustache', 'r') as f:
            body = chevron.render(f, {'keyword': keyword_str, 'theme': theme_str})
            graph.parse(data=body, format="turtle")

        post_body = graph.serialize(format='turtle')
        dataset_url = self.FDP_CLIENT.fdp_create_metadata(post_body, "dataset")
        print("New dataset created : " + dataset_url)
        return dataset_url

    def create_distribution(self, distribution):
        """
        Method to create distribution in FDP

        :param distribution: Provide distribution object
        :return: FDP's distribution URL
        """
        parent_url = distribution.PARENT_URL

        if not self.FDP_CLIENT.does_metadata_exists(parent_url):
            raise SystemExit("The dataset <"+parent_url+"> doesn't exist. Provide valid dataset URL")

        graph = Graph()

        # create resource triples
        self.UTILS.add_resource_triples(distribution, graph)
        # Create language triples
        self.UTILS.add_language_triples(distribution, graph)
        # Create license triples
        self.UTILS.add_licence_triples(distribution, graph)

        # Create byte size triples
        if distribution.BYTE_SIZE:
            with open('../templates/bytesize.mustache', 'r') as f:
                body = chevron.render(f, {'byte_size': distribution.BYTE_SIZE})
                graph.parse(data=body, format="turtle")

        # Create format triples
        if distribution.FORMAT:
            with open('../templates/format.mustache', 'r') as f:
                body = chevron.render(f, {'format': distribution.FORMAT})
                graph.parse(data=body, format="turtle")

        distribution_url = None
        distribution_type = None

        if distribution.ACCESS_URL:
            distribution_type = "dcat:accessURL"
            distribution_url = distribution.ACCESS_URL
        elif distribution.DOWNLOAD_URL:
            distribution_type = "dcat:downloadURL"
            distribution_url = distribution.DOWNLOAD_URL

        # create distribution triples
        with open('../templates/distribution.mustache', 'r') as f:
            body = chevron.render(f, {'distribution_type': distribution_type, 'distribution_url': distribution_url,
                                      'media_type': distribution.MEDIA_TYPE})
            graph.parse(data=body, format="turtle")

        post_body = graph.serialize(format='turtle')
        metadata_url = self.FDP_CLIENT.fdp_create_metadata(post_body, "distribution")
        print("New distribution created : " + metadata_url)
        return metadata_url

    def create_organisation(self, organisation):
        """
        Method to create organisation in FDP

        :param biobank: Provide organisation object
        :return: FDP's organisation URL
        """
        parent_url = organisation.PARENT_URL

        if not self.FDP_CLIENT.does_metadata_exists(parent_url):
            raise SystemExit("The catalog <"+parent_url+"> doesn't exist. Provide valid catalog URL")

        print("The catalog <"+parent_url+"> exist")

        # Create pages list
        page_str = ""
        for page in organisation.LANDING_PAGES:
            page_str = page_str + " <" + page + ">,"
        page_str = page_str[:-1]

        # Render RDF
        graph = Graph()

        with open('../templates/organisation.mustache', 'r') as f:
            body = chevron.render(f, {'parent_url': organisation.PARENT_URL,
                                      'title': organisation.TITLE,
                                      'description': organisation.DESCRIPTION,
                                      'location_title': organisation.LOCATION_TITLE,
                                      'location_description': organisation.LOCATION_DESCRIPTION,
                                      'pages': page_str})
            graph.parse(data=body, format="turtle")

        # Serialize RDF and send to FDP
        post_body = graph.serialize(format='turtle')
        print(post_body)
        organisation_url = self.FDP_CLIENT.fdp_create_metadata(post_body, "organisation")
        print("New organisation created : " + organisation_url)
        return organisation_url

    def create_biobank(self, biobank):
        """
        Method to create biobank in FDP

        :param biobank: Provide biobank object
        :return: FDP's biobank URL
        """
        parent_url = biobank.PARENT_URL

        if not self.FDP_CLIENT.does_metadata_exists(parent_url):
            raise SystemExit("The catalog <"+parent_url+"> doesn't exist. Provide valid catalog URL")

        print("The catalog <"+parent_url+"> exist")


        # Create themes list
        theme_str = ""
        for theme in biobank.THEMES:
            theme_str = theme_str + " <" + theme + ">,"
        theme_str = theme_str[:-1]

        # Create pages list
        page_str = ""
        for page in biobank.LANDING_PAGES:
            page_str = page_str + " <" + page + ">,"
        page_str = page_str[:-1]

        # Render RDF
        graph = Graph()

        with open('../templates/biobank.mustache', 'r') as f:
            body = chevron.render(f, {'parent_url': biobank.PARENT_URL,
                                      'title': biobank.TITLE,
                                      'description': biobank.DESCRIPTION,
                                      'populationcoverage': biobank.POPULATIONCOVERAGE,
                                      'themes': theme_str,
                                      'publisher': biobank.PUBLISHER_URL,
                                      'pages': page_str})
            graph.parse(data=body, format="turtle")

        # Serialize RDF and send to FDP
        post_body = graph.serialize(format='turtle')
        print(post_body)
        biobank_url = self.FDP_CLIENT.fdp_create_metadata(post_body, "biobank")
        print("New biobank created : " + biobank_url)
        return biobank_url

    def create_patientregistry(self, patientregistry):
        """
        Method to create patient registry in FDP

        :param patient registry: Provide patient registry object
        :return: FDP's patient registry URL
        """
        parent_url = patientregistry.PARENT_URL

        if not self.FDP_CLIENT.does_metadata_exists(parent_url):
            raise SystemExit("The catalog <"+parent_url+"> doesn't exist. Provide valid catalog URL")

        print("The catalog <"+parent_url+"> exist")


        # Create themes list
        theme_str = ""
        for theme in patientregistry.THEMES:
            theme_str = theme_str + " <" + theme + ">,"
        theme_str = theme_str[:-1]

        # Create pages list
        page_str = ""
        for page in patientregistry.LANDING_PAGES:
            page_str = page_str + " <" + page + ">,"
        page_str = page_str[:-1]

        # Render RDF
        graph = Graph()

        with open('../templates/patientregistry.mustache', 'r') as f:
            body = chevron.render(f, {'parent_url': patientregistry.PARENT_URL,
                                      'title': patientregistry.TITLE,
                                      'description': patientregistry.DESCRIPTION,
                                      'populationcoverage': patientregistry.POPULATIONCOVERAGE,
                                      'themes': theme_str,
                                      'publisher': patientregistry.PUBLISHER_URL,
                                      'pages': page_str})
            graph.parse(data=body, format="turtle")

        # Serialize RDF and send to FDP
        post_body = graph.serialize(format='turtle')
        print(post_body)
        patientregistry_url = self.FDP_CLIENT.fdp_create_metadata(post_body, "patientregistry")
        print("New patient registry created : " + patientregistry_url)
        return patientregistry_url