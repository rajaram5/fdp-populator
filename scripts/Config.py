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
EJP_VP_INPUT_FILE = None
DRY_RUN = None
CATALOG_URL = None
CONFIG_FILE = os.environ['CONFIG_FILE']
BASE_PATH = os.environ['BASE_PATH']

if os.path.isfile(CONFIG_FILE) :
    yaml_file = open(CONFIG_FILE)
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

    # Check for FDP template configuration
    try:
        DATASET_INPUT_FILE = os.path.join(BASE_PATH, config['dataset_file'])
        DISTRIBUTION_INPUT_FILE = os.path.join(BASE_PATH, config['distribution'])
    except:
        pass

    # Check for VP template configuration
    try:
        EJP_VP_INPUT_FILE = os.path.join(BASE_PATH, config['ejp_vp_file'])
    except:
        pass

    try:
        DRY_RUN = config['dry_run']
        if DRY_RUN not in (True, False):
            DRY_RUN = False
    except:
        DRY_RUN = False

    CATALOG_URL = config['catalog_url']
else:
    raise SystemExit("Config file does not exist. Provided input file path: " + CONFIG_FILE)