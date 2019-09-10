import pytoml
import json
import os
from PIL import Image

source = './team'
target = '../www_threefold.io_new/data.js'
avatars_dir = "../www_threefold.io_new/avatars"
section = []

for name in os.listdir(source):
    if os.path.isdir(os.path.join(source, name)):
        child = os.path.join(source, name)
        image = "image.jpg"
        for filename in os.listdir(child):
            if filename.endswith((".jpg", ".JPG")):
                image = filename
                continue

            if not filename.endswith(".toml"):
                continue

            # print("Processing: %s" % child)

            with open(os.path.join(child, filename), 'r') as f:
                person = pytoml.load(f)
                full_name = person.get('full_name')
                description = person.get('description')
                function = person.get('function')
                project_ids = person.get('project_ids')
                contribution_ids = person.get('contribution_ids')
                nationality = person.get('nationality')

            if image:
                img = Image.open(os.path.join(child, image))
                if img.height != img.width:
                    side = min((img.width, img.height))
                    img = img.crop((0, 0, side, side))

                side = 252
                if img.height != side:
                    img = img.resize((side, side))

                avatar_filename = os.path.join(avatars_dir, image)
                img.save(avatar_filename)
                avatar_name = "processed_" + image
                print('child: {}'.format(child))
                print('filename: {}'.format(filename))
                print('avatar name: {}'.format(avatar_name))
                # else:
                #     avatar_name = "processed_" + image
                #     print('child: {}'.format(child))
                #     print('filename: {}'.format(filename))
                #     print('avatar name: {}'.format(avatar_name))

                section.append({
                    "full_name": full_name,
                    "description": description,
                    "function": function,
                    "project_ids": project_ids,
                    "contribution_ids": contribution_ids,
                    "nationality": nationality,
                    "avatar": avatar_name
                })

with open(target, 'w') as f:
    f.write("var team = ")
    f.write(json.dumps(section))
    f.write(";\n")
