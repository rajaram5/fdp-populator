import FDPClient
import Config
import chevron
import csv
from rdflib import Graph

"""
Class to populate FDP with content
"""

class Populator:
    FDP_CLIENT = FDPClient.FDPClient(Config.FDP_URL, Config.FDP_USERNAME, Config.FDP_PASSWORD,
                                     Config.FDP_PERSISTENT_URL)
    """
    Method to create catalogs in FDP. This FDP uses catalog.csv file
    """
    def create_catalogs(self):
        reader = csv.reader(open(Config.INPUT_FILE, 'r'))
        line = 0
        for row in reader:
            if line > 0:
                print(row)
                catalog_title = row[0]
                catalog_publisher = row[1]

                # create catalog
                with open('templates/catalog.mustache', 'r') as f:
                    catalog_body = chevron.render(f, {'publisher': catalog_publisher, 'title': catalog_title,
                                                      'fdp_url': Config.FDP_URL})
                    fdp_catalog_url = self.FDP_CLIENT.fdp_create_metadata(catalog_body, "catalog")
                    print("New catalog created : " + fdp_catalog_url)
            line = line + 1

    """
        Method to create catalogs in FDP. This FDP uses catalog.csv file
        """

    def create_datasets(self):
        reader = csv.reader(open(Config.DATASET_INPUT_FILE, 'r'))

        line = 0
        for row in reader:
            if line > 0:
                print(row)
                graph = Graph()
                title = row[0]
                parent_url = row[1]
                publisher_url = row[2]
                description = row[3]
                language = row[4]
                license = row[5]
                contact_point = row[6]
                landing_page = row[7]
                keywords = row[8]
                themes = row[9]

                if not description:
                    description = "Metadata od dataset " + title

                # Create language triples
                if language:
                    language_url = "http://id.loc.gov/vocabulary/iso639-1/" + language.strip()
                    with open('templates/language.mustache', 'r') as f:
                        body = chevron.render(f, {'language_url': language_url})
                        graph.parse(data=body, format="turtle")

                # Create license triples
                if license:
                    license_url = license.strip()
                    with open('templates/license.mustache', 'r') as f:
                        license_body = chevron.render(f, {'license_url': license_url})
                        graph.parse(data=body, format="turtle")

                # Create license triples
                if landing_page:
                    landing_page_url = landing_page.strip()
                    with open('templates/landingpage.mustache', 'r') as f:
                        body = chevron.render(f, {'page_url': landing_page_url})
                        graph.parse(data=body, format="turtle")

                # Create contact point triples
                if contact_point:
                    contact_point_url = contact_point.strip()
                    with open('templates/contact.mustache', 'r') as f:
                        body = chevron.render(f, {'contact_url': contact_point_url})
                        graph.parse(data=body, format="turtle")

                # Create keywords list
                keyword_str = ""
                for keyword in keywords.split(","):
                    keyword = keyword.strip()
                    keyword_str = keyword_str + ' "' + keyword + '",'
                keyword_str = keyword_str[:-1]

                # Create themes list
                theme_str = ""
                for theme in themes.split(","):
                    theme = theme.strip()
                    theme_str = theme_str + " <" + theme + ">,"
                theme_str = theme_str[:-1]

                # create dataset triples
                with open('templates/dataset.mustache', 'r') as f:
                    body = chevron.render(f, {'keyword': keyword_str, 'theme': theme_str})
                    graph.parse(data=body, format="turtle")

                # create resource triples
                with open('templates/resource.mustache', 'r') as f:
                    body = chevron.render(f, {'description': description, 'title': title,
                                              'parent_url': parent_url, 'publisher_url': publisher_url,
                                              'publisher_name': publisher_url})
                    graph.parse(data=body, format="turtle")

                post_body = (graph.serialize(format='turtle')).decode("utf-8")
                dataset_url = self.FDP_CLIENT.fdp_create_metadata(post_body, "dataset")
                print("New dataset created : " + dataset_url)
            line = line + 1
