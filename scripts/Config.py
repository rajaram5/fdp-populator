import os
import glob
import yaml

print("Files from the parent dir : " + str(glob.glob("*")))

FDP_URL = os.environ['FDP_URL']
FDP_USERNAME = os.environ['FDP_USERNAME']
FDP_PASSWORD = os.environ['FDP_PASSWORD']
FDP_PERSISTENT_URL = os.environ['FDP_PERSISTENT_URL']
DATASET_INPUT_FILE = None
DISTRIBUTION_INPUT_FILE = None
CATALOG_URL = None
CONFIG_FILE = os.environ['CONFIG_FILE']
BASE_PATH = os.environ['BASE_PATH']

if os.path.isfile(CONFIG_FILE) :
    yaml_file = open(CONFIG_FILE)
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)
    DATASET_INPUT_FILE = BASE_PATH + config['dataset_file']
    DISTRIBUTION_INPUT_FILE = BASE_PATH + config['distribution']
    CATALOG_URL = config['catalog_url']
else:
    raise SystemExit("Config file does exits. Provided input file " + CONFIG_FILE)