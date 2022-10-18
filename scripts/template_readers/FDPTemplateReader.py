import Config
import csv
from resource_classes import Dataset, Distribution


class FDPTemplateReader:
    """
    NOTE: this class is based on the folling specification:
    <https://github.com/LUMC-BioSemantics/EJP-RD-WP19-FDP-template>
    """
    def get_datasets(self):
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

    def get_distributions(self):
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
                dataset_name = row[1]
                publisher_url = row[2]
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