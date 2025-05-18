# DATABASE
# DB_HOST = "172.17.0.1"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "channelsdb"
DB_USER = "channelsdb"
DB_PASSWORD = "admin"

# API
API_PATH = "/api/v1"

# MIRROR API
MIRROR_API_PATH = "http://172.17.0.1:8001/api/v1/"
MIRROR_API_LIMIT = 10

# PDB API
PDB_HTTP_FILE_URL = (
    "https://files-versioned.wwpdb.org/pdb_versioned/views/all/coordinates/mmcif/"
)
PDB_HTTP_TIMEOUT = 5  # Seconds.
PDB_HTTP_ASSEMBLY_URL = "https://www.ebi.ac.uk/pdbe/api/pdb/entry/summary/"
PDB_HTTP_IMAGE_URL = "https://www.ebi.ac.uk/pdbe/static/entry/|protein_id|_assembly_|assembly_id|_chemically_distinct_molecules_front_image-200x200.png"

PDB_DATA_API_URL = "https://data.rcsb.org/graphql"

PDB_SEARCH_API_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
PDB_SEARCH_API_LIMIT = 20

PDB_FTP_STATUS_URL = "https://files.rcsb.org/pub/pdb/data/status/"

# ALPHAFILL
ALPHAFILL_HTTP_FILE_URL = "https://alphafill.eu/v1/aff/"

# MULTIPROCESSING
QUEUE_TIMEOUT = 2
QUEUE_SIZE = 10
MANAGER_LIMIT = 5
WORKER_LIMIT = 100
CRON_JOB_DAY = 3  # 0-6 (Mon - Sun).

# DIRECTORIES
CONFIG_PATH = "./app/channels/commands/config"
OUTPUT_PATH = "./app/channels/output"
RELATIVE_MOLE_PATH = "../../commands/mole2/mole2.exe"
