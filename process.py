import pytoml
import json
import os
from PIL import Image

source = './team'
target = '../www_threefold.io_new_b/js/data.js'
avatars_dir = "../www_threefold.io_new_b/avatars"
section = []

all_files = {}
for name in os.listdir(source):
    if os.path.isdir(os.path.join(source, name)):
        child = os.path.join(source, name)
        all_files[child] = {'image': "image.jpg"}
        for filename in os.listdir(child):
            if filename.endswith((".jpg", ".JPG")):
                all_files[child]['image'] = filename
            elif filename.endswith(".toml"):
                all_files[child]['toml'] = filename

for child, files in all_files.items():
    print("Processing: %s" % child)

    with open(os.path.join(child, files['toml']), 'r') as f:
        person = pytoml.load(f)
        full_name = person.get('full_name')
        description = person.get('description')
        function = person.get('function')
        project_ids = person.get('project_ids')
        contribution_ids = person.get('contribution_ids')
        nationality = person.get('nationality')
        
        if files['image'] != "image.jpg":
            img = Image.open(os.path.join(child, files['image']))
            if img.height != img.width:
                side = min((img.width, img.height))
                img = img.crop((0, 0, side, side))

            side = 252
            if img.height != side:
                img = img.resize((side, side))

            avatar_filename = os.path.join(avatars_dir, files['image'])
            img.save(avatar_filename)
            avatar_name = files['image']
        else:
            avatar_name = files['image']

        section.append({"full_name":full_name, "description":description, "function":function, "project_ids":project_ids,
                       "contribution_ids":contribution_ids, "nationality":nationality, "avatar":avatar_name})

with open(target, 'w') as f:
    f.write("var team = ")
    f.write(json.dumps(section))
    f.write(";\n")
