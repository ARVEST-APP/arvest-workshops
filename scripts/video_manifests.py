import iiif_prezi3
from jhutils.local_files import get_video_info, get_image_info, write_json
from jhutils.online_files import download
import os
import arvestapi

SOURCE_MEDIA_TITLE = "Scene B (Café Müller, Pina Bausch) | From the film Pina (2011)"
MANIFEST_FILE_NAME = "scene_b_2011"
MANIFEST_DATA = {
    "name" : "Scene B (Café Müller, Pina Bausch) | From the film Pina (2011)",
    "metadata" : [
        {"label":{"en":["Year"]},"value":{"en":["2011"]}}
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

OUTPUT_FOLDER = os.path.join(os.getcwd(), "resources", "manifests", "videos")
ID_PREFIX = "https://raw.githubusercontent.com/ARVEST-APP/arvest-workshops/refs/heads/main"

# Make output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ar = arvestapi.Arvest("arvestuser@gmail.com", "arvestworkshop000")
medias = ar.get_medias()
media_to_treat = None
for media in medias:
    if media.title == SOURCE_MEDIA_TITLE:
        media_to_treat = media

if media_to_treat != None:

    temp_path = os.path.join(os.getcwd(), "_TEMP")
    os.makedirs(temp_path, exist_ok = True)
    local_source_path = download(media_to_treat.get_full_url(), dir = temp_path)

    man = iiif_prezi3.Manifest(
        id = os.path.join(ID_PREFIX, "resources", "manifests", "videos", f"{MANIFEST_FILE_NAME}.json"),
        label = {"en" : [MANIFEST_DATA["name"]]}
    )
    man.metadata = MANIFEST_DATA["metadata"]
    man.rights = MANIFEST_DATA["rights"]
    man.requiredStatement = MANIFEST_DATA["requiredStatement"]
    man.provider = MANIFEST_DATA["provider"]

    thumb_local = download(media_to_treat.thumbnail_url, dir = temp_path)
    thumb_info = get_image_info(thumb_local)
    man.thumbnail = [{"id" : media_to_treat.thumbnail_url, "type" : "Image", "format" : "image/webp", "width" : thumb_info["width"], "height" : thumb_info["height"]}]

    source_info = get_video_info(local_source_path)
    can = iiif_prezi3.Canvas(
        id = os.path.join(ID_PREFIX, "resources", "manifests", "videos", MANIFEST_FILE_NAME, "canvas", "1"),
        label = {"en":[f"{MANIFEST_DATA['name']}"]},
        width = source_info["width"],
        height = source_info["height"],
        duration = source_info["duration"] / 1000
    )
    can.thumbnail = [{"id" : media_to_treat.thumbnail_url, "type" : "Image", "format" : "image/webp", "width" : thumb_info["width"], "height" : thumb_info["height"]}]

    anpa = iiif_prezi3.AnnotationPage(
        id = os.path.join(ID_PREFIX, "resources", "manifests", "videos", MANIFEST_FILE_NAME, "canvas", "1", "page", "1")
    )

    an = iiif_prezi3.Annotation(
        id = os.path.join(ID_PREFIX, "resources", "manifests", "videos", MANIFEST_FILE_NAME, "canvas", "1", "page", "1", "1"),
        motivation = "painting",
        target = os.path.join(ID_PREFIX, "resources", "manifests", "videos", MANIFEST_FILE_NAME, "canvas", "1") + f"#xywh=0,0,{source_info['width']},{source_info['height']}&t=0,{source_info['duration'] / 1000}"
    )
    an.body = {
        "id" : media_to_treat.get_full_url(),
        "type" : "Video",
        "width" : source_info["width"],
        "height" : source_info["height"],
        "duration" : source_info["duration"] / 1000,
        "format" : "video/MPG"
    }

    anpa.items.append(an)
    can.items.append(anpa)
    man.items.append(can)

    man_as_dict = man.dict()
    man_as_dict["logo"] = MANIFEST_DATA["logo"]

    write_json(os.path.join(OUTPUT_FOLDER, f"{MANIFEST_FILE_NAME}.json"), man_as_dict)