import iiif_prezi3
from jhutils.local_files import get_image_info, write_json, collect_files
import os
from PIL import Image

SOURCE_FOLDER = "resources/imgs/programmes/Programme2023"
MANIFEST_FILE_NAME = "Programme2023"
MANIFEST_DATA = {
    "name" : "Programme 2023",
    "metadata" : [
        {"label":{"en":["Year"]},"value":{"en":["2023"]}}
    ],
    "logo" : {
        "id": "https://raw.githubusercontent.com/ARVEST-APP/arvest-workshops/refs/heads/main/resources/imgs/rennes2-logo.png",
        "type": "Image",
        "format": "image/png",
        "height": 225,
        "width": 225
    },
    "rights": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
    "requiredStatement": {"label": {"en": ["Attribution"]},"value": {"en": ["Rennes 2 University"]}},
    "provider": [{
      "id": "https://www.univ-rennes2.fr/",
      "type": "Agent",
      "label": {"en": ["Rennes 2 University"]},
      "homepage": [{"id": "https://www.univ-rennes2.fr/","type": "Text","label": {"en": ["Rennes 2 University"]},"format": "text/html"}]
    }]
}

OUTPUT_FOLDER = os.path.join(os.getcwd(), "resources", "manifests", "programmes")
ID_PREFIX = "https://raw.githubusercontent.com/ARVEST-APP/arvest-workshops/refs/heads/main"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

man = iiif_prezi3.Manifest(
    id = os.path.join(ID_PREFIX, "resources", "manifests", "programmes", f"{MANIFEST_FILE_NAME}.json"),
    label = {"en" : [MANIFEST_DATA["name"]]}
)
man.metadata = MANIFEST_DATA["metadata"]
man.rights = MANIFEST_DATA["rights"]
man.requiredStatement = MANIFEST_DATA["requiredStatement"]
man.provider = MANIFEST_DATA["provider"]

# make thumbnails:
image_files = collect_files(os.path.join(os.getcwd(), SOURCE_FOLDER), ["png"])
os.makedirs(os.path.join(os.getcwd(), SOURCE_FOLDER, "thumbnails"), exist_ok=True)
first_thumb = None
for i, image_file in enumerate(image_files):
    img = Image.open(image_file)
    file_name = os.path.splitext(os.path.basename(image_file))[0]
    thumbnail_size = (128, 128)
    img.thumbnail(thumbnail_size)
    img.save(os.path.join(os.getcwd(), SOURCE_FOLDER, "thumbnails", f"{file_name}.jpg"))
    if i == 0:
        first_thumb = f"{file_name}.jpg"
thumb_info = get_image_info(os.path.join(os.getcwd(), SOURCE_FOLDER, "thumbnails", first_thumb))
man.thumbnail = [{"id" : os.path.join(ID_PREFIX, SOURCE_FOLDER, "thumbnails", first_thumb), "type" : "Image", "format" : "image/jpg", "width" : thumb_info["width"], "height" : thumb_info["height"]}]

# Add pages:
for i, image_file in enumerate(image_files):
    base_name = os.path.basename(image_file)
    file_name = os.path.splitext(base_name)[0]
    thumbnail_url = os.path.join(ID_PREFIX, SOURCE_FOLDER, "thumbnails", f"{file_name}.jpg")
    thumbnail_path = os.path.join(os.getcwd(), SOURCE_FOLDER, "thumbnails", f"{file_name}.jpg")
    
    source_info = get_image_info(image_file)
    thumbnail_info = get_image_info(thumbnail_path)

    can = iiif_prezi3.Canvas(
        id = os.path.join(ID_PREFIX, "resources", "manifests", "programmes", MANIFEST_FILE_NAME, "canvas", str(i + 1)),
        label = {"en":[f"{MANIFEST_DATA['name']} (page {str(i + 1)})"]},
        width = source_info["width"],
        height = source_info["height"]
    )
    can.thumbnail = [{"id" : thumbnail_url, "type" : "Image", "format" : "image/jpg", "width" : thumbnail_info["width"], "height" : thumbnail_info["height"]}]

    anpa = iiif_prezi3.AnnotationPage(
        id = os.path.join(ID_PREFIX, "resources", "manifests", "programmes", MANIFEST_FILE_NAME, "canvas", str(i + 1), "page", "1")
    )

    an = iiif_prezi3.Annotation(
        id = os.path.join(ID_PREFIX, "resources", "manifests", "programmes", MANIFEST_FILE_NAME, "canvas", str(i + 1), "page", "1", "1"),
        motivation = "painting",
        target = os.path.join(ID_PREFIX, "resources", "manifests", "programmes", MANIFEST_FILE_NAME, "canvas", str(i + 1)) + f"#xywh=0,0,{source_info['width']},{source_info['height']}"
    )
    an.body = {
        "id" : os.path.join(ID_PREFIX, SOURCE_FOLDER, os.path.basename(image_file)),
        "type" : "Image",
        "width" : source_info["width"],
        "height" : source_info["height"],
        "format" : "image/png"
    }

    anpa.items.append(an)
    can.items.append(anpa)
    man.items.append(can)

man_as_dict = man.dict()
man_as_dict["logo"] = MANIFEST_DATA["logo"]

write_json(os.path.join(OUTPUT_FOLDER, f"{MANIFEST_FILE_NAME}.json"), man_as_dict)