import iiif_prezi3
from jhutils.local_files import get_image_info, write_json
import os

SOURCE_FOLDER = "/Users/jacob/Documents/Repos/ARVEST-APP/arvest-workshops/resources/imgs/programmes/Avignon1995"
OUTPUT = os.path.join(os.getcwd(), "resouces", "manifests", "programmes", "Avignon1995.json")

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)