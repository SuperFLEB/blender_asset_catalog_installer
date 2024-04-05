"""
┈─┬──────────────────────────────╮
╭───○ ASSET CATALOG SETUP SCRIPT │
│ ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┈
│                                ╰──────────────────────────────────────────────────────────────────────────────────────┈
╰▷ This file comes with catalog information for use in the Asset Browser.
   To assign Asset Browser catalogs for these assets, run this script:

    1.) Copy this .blend file to your asset library directory (if you haven't already)
    2.) Open the copy of the .blend file in your asset library directory (if you haven't already)
    3.) View this script (If you can read this, you currently are)
    4.) Run this script using the "Text > Run Script" menu item, Alt+P, or the "▶" button at the top of this panel.


Alternatively, find the blender_assets.cats.txt Text item (in the menu above) and manually combine the contents
with the blender_assets.cats.txt file in your asset library (or copy it all to a new one, if none exists).

┈────────────────────────────────╮ ┈────────────────────────────────────────────────────────────────────────────────────┈
┈─────────────────────────────── ╰────────────────────────────────────────────────────────────────────────────────────────┈



























"""

# Python script to copy or integrate the packed blender_assets.cats.txt Text datablock with the external
# blender_assets.cats.txt file.

import bpy
import re
import shutil
from bpy.path import abspath
from os.path import isfile

# If version 2 or whatever comes around and it's compatible, just bump this number to make the script work
MAX_CATSFILE_VERSION = 1

cat_file_path = abspath('//blender_assets.cats.txt')
backup_file_path = abspath('//blender_assets.cats.backup.txt')


def get_cats_by_uuid(catfile: str) -> dict[str, str]:
    lines = catfile.split('\n')
    uuids = {}
    for line in lines:
        match = re.search('([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}):.+', line)
        if not match:
            continue
        uuid = match.group(1)
        uuids[uuid] = line
    return uuids


def just_dump():
    """
    Copy the blender_assets.cats.txt textblock from this .blend file to an external file.
    """
    if not 'blender_assets.cats.txt' in bpy.data.texts:
        raise Exception('Internal error: Cannot find text datablock blender_assets.cats.txt')
    fh = open(cat_file_path, 'x')
    fh.write(bpy.data.texts['blender_assets.cats.txt'].as_string())
    fh.close()
    print(f"Created new file at {cat_file_path}")


def add_unseen():
    """
    Add UUIDs from the blender_assets.cats.txt textblock from this .blend file to the external
    blender_assets.cats.txt file if they are not already present
    """

    if not 'blender_assets.cats.txt' in bpy.data.texts:
        raise Exception('Internal error: Cannot find text datablock blender_assets.cats.txt')

    # Read existing information and find new UUIDs
    fh = open(cat_file_path, 'r')
    existing_cats_file = fh.read()
    fh.close()

    version_lines = [line for line in existing_cats_file.split('\n') if re.match('^VERSION \d+$', line)]
    if not version_lines:
        raise Exception('Cannot find VERSION in blender_assets.cats.txt file. It may be a newer version, or invalid.')

    version = int(version_lines[0][8:])

    print(
        f"Updating catalog file at {cat_file_path}.\nFile is version {version}. Max supported is version {MAX_CATSFILE_VERSION}.")

    if version > MAX_CATSFILE_VERSION:
        raise Exception(
            f"VERSION in blender_assets.cats.txt file is version {version} and may not be compatible with version {MAX_CATSFILE_VERSION}. Change MAX_CATSFILE_VERSION in the script if you want to try it.")

    existing_cats = get_cats_by_uuid(existing_cats_file)
    my_cats = get_cats_by_uuid(bpy.data.texts['blender_assets.cats.txt'].as_string())
    new_cats = {uuid: spec for (uuid, spec) in my_cats.items() if uuid not in existing_cats}

    new_lines = [line for line in new_cats.values()]

    if not new_lines:
        print("No new catalog items to add. Nothing done.")
        return

    # Make a backup
    shutil.copyfile(cat_file_path, backup_file_path)
    print(f"Created backup catalog file at {backup_file_path}")

    # Write the new lines
    fh = open(cat_file_path, 'a')
    fh.write('\n'.join(new_lines))
    fh.close()
    print(f"Updated catalog file at {cat_file_path}")


def main():
    message = ""

    def draw(self, _):
        self.layout.label(text=message)

    try:
        if not isfile(abspath('//blender_assets.cats.txt')):
            just_dump()
            message = "Created a catalog file"
        else:
            add_unseen()
            message = "Added new catalogs"
        bpy.context.window_manager.popup_menu(draw, title="OK")
    except Exception as e:
        message = str(e)
        bpy.context.window_manager.popup_menu(draw, title="Error")


if __name__ == "__main__":
    main()
