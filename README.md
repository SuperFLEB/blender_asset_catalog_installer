# Blender Asset Catalog Installer

https://github.com/SuperFLEB/blender_asset_catalog_installer

This is a script you can add to your asset files to allow "installing" asset catalogs to users' Asset Library. The asset
creator can set up the Asset Catalog structure in the file, which creating a `blender_assets.cats.txt` file, then append
that as a Text block in the .blend file. The end user can run the script, which will add the Catalog definitions
from the `blender_assets.cats.txt` in the .blend file into the existing `blender_assets.cats.txt` and into the
Asset Library.

_This is not a Blender addon or standalone script. It is meant to be included in asset .blend files you distribute._

## To Use (as the asset creator)

1. Mark your Assets
    - Mark the assets in your file using the Mark as Asset function. Save your file.
2. Organize Catalogs
   - In the Asset Browser, add a hierarchy of Asset Catalogs (in "Current File") and put your individual assets
     into them.
3. Save Asset Catalogs
   - Click "Save Asset Catalog" to write the catalog file
4. Copy the asset file into your .blend file
   - In the Text editor (Scripting workspace), open the file `blender_assets.cats.txt` from the same directory as your
     .blend file. This should add the `blender_assets.cats.txt` file into your .blend file.
5. Copy the `Catalog Setup` script into your .blend file.
   - In the Text editor, open the file `Catalog Setup.py` from this repository into your .blend file.
   - You may remove the `.py` extension for simplicity's sake. It will still work the same.

Now, instruct your asset's users to run the `Catalog Setup` Text block in the .blend file.
(Instructions are in a docstring in the script.)

## To Use (as the Asset end-user)

_Instructions for using the script are in the script itself._

1. Copy the .blend file into an Asset Library directory.
2. Open the .blend file in the Asset Library directory.
3. Switch to the "Catalog Setup" script in the Text Editor
4. Run the script, using the menu, Alt-P, or the "▶" button.

