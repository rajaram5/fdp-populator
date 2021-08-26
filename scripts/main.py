import chevron
import FDPClient
import Config
import csv

FDP_CLIENT = FDPClient.FDPClient(Config.FDP_URL, Config.FDP_USERNAME, Config.FDP_PASSWORD, Config.FDP_PERSISTENT_URL)

def populate_fdp_metdata():
    reader = csv.reader(open(Config.INPUT_FILE, 'r'))
    line = 0
    for row in reader:
        if line > 0:
            print(row)
            catalog_title = row[0]
            catalog_publisher= row[1]

            # create catalog
            with open('templates/catalog.mustache', 'r') as f:
                catalog_body = chevron.render(f, {'publisher': catalog_publisher, 'title': catalog_title,
                                                  'fdp_url': Config.FDP_URL})
                fdp_catalog_url = FDP_CLIENT.fdp_create_metadata(catalog_body, "catalog")
                print("New catalog created : " + fdp_catalog_url)
        line = line + 1


populate_fdp_metdata()