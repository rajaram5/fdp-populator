import FDPClient
import Dataset
import Config
import chevron
import csv
import Utils
import Distribution
from rdflib import Graph



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
        # GET datasets
        datasets = self.__get_datasets__()
        # GET distributions
        distributions = self.__get_distributions__()
        # Populate FDP with datasets
        for dataset_name, dataset in datasets.items():
            dataset_url = self.create_dataset(dataset)
            if dataset_name in distributions:
                distribution = distributions[dataset_name]
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

        post_body = (graph.serialize(format='turtle')).decode("utf-8")
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

        post_body = (graph.serialize(format='turtle')).decode("utf-8")
        metadata_url = self.FDP_CLIENT.fdp_create_metadata(post_body, "distribution")
        print("New distribution created : " + metadata_url)
        return metadata_url

    """
    """
    def __get_datasets__(self):
        """
        This method creates datasets objects by extracting content from the dataset input CSV file.
        NOTE: This method assumes that provided input file follows this spec
        <https://github.com/LUMC-BioSemantics/EJP-RD-WP19-FDP-template>

        :return: Dict of datasets
        """

        reader = csv.reader(open(Config.DATASET_INPUT_FILE, 'r'))
        catalog_url = Config.CATALOG_URL
        datasets = {}
        for row in reader:
            if reader.line_num > 1:
                print(row)
                title = row[0]
                publisher_url = row[1]
                description = row[2]
                language = row[3]
                license = row[4]
                contact_point = row[5]
                landing_page = row[6]
                keywords_str = row[7]
                themes_str = row[8]
                language_url = None
                license_url = None
                landing_page_url = None
                contact_point_url = None

                if not description:
                    description = "Metadata od dataset " + title
                # Create language triples
                if language:
                    language_url = "http://id.loc.gov/vocabulary/iso639-1/" + language.strip()
                # Create license triples
                if license:
                    license_url = license.strip()
                # Create license triples
                if landing_page:
                    landing_page_url = landing_page.strip()
                # Create contact point triples
                if contact_point:
                    contact_point_url = contact_point.strip()
                # Create keywords list
                keywords = []
                for keyword in keywords_str.split(","):
                    keyword = keyword.strip()
                    keywords.append(keyword)
                # Create themes list
                themes = []
                for theme in themes_str.split(","):
                    theme = theme.strip()
                    themes.append(theme)
                dataset = Dataset.Dataset(catalog_url, title, description, keywords, themes, publisher_url,
                                          language_url, license_url, landing_page_url, contact_point_url)
                datasets[title] = dataset
        return datasets

    def __get_distributions__(self):
        """
        This method creates distribution objects by extracting content from the distribution input CSV file.
        NOTE: This method assumes that provided input file follows this spec
        <https://github.com/LUMC-BioSemantics/EJP-RD-WP19-FDP-template>

        :return: Dict of distribution
        """

        reader = csv.reader(open(Config.DISTRIBUTION_INPUT_FILE, 'r'))
        distributions = {}
        for row in reader:
            if reader.line_num > 1:
                print(row)
                title = row[0]
                publisher_url = row[1]
                dataset_name = row[2]
                description = row[3]
                language = row[4]
                license = row[5]
                access_url = row[6]
                download_url = row[7]
                media_type = row[8]
                compression_format = row[9]
                format = row[10]
                byte_size = row[11]
                language_url = None
                license_url = None

                if not description:
                    description = "Metadata od dataset " + title
                # Create language triples
                if language:
                    language_url = "http://id.loc.gov/vocabulary/iso639-1/" + language.strip()
                # Create license triples
                if license:
                    license_url = license.strip()
                distribution = Distribution.Distribution(None, title, description, publisher_url, language_url,
                                                         license_url, access_url, download_url, media_type,
                                                         compression_format, format, byte_size, dataset_name)
                distributions[title] = distribution
        return distributions

