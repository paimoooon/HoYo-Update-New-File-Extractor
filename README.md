# HoYo Update New File Extractor

Extract newly added files for each upate. Only tested on a dead game yet.

### Prerequisite

- [HoYoStudio 0.80.60](https://gitlab.com/RazTools/Studio/-/releases/v0.80.60)
- tqdm
  ```apache
  pip install tqdm
  ```

---



### How To Use

1. Build the AssetMap XML files for the old and new clients.

   - In AssetStuidioGUI:  `Misc.` → `Build AssetMap`
   - By [HoYoStudio 0.18.60 CLI](https://gitlab.com/RazTools/Studio/-/releases/v0.18.60):
     Change the constants in `assetmap_xml_extract.py` and then run the script. Note that [HoYoStudio 0.80.60](https://gitlab.com/RazTools/Studio/-/releases/v0.80.60)'s CLI doesn't work.
2. Rename them to `old_assetmap.xml` and `new_assetmap.xml`, then move them into the `./input` folder. They will already be there if you used the `assetmap_xml_extract.py` method.
3. Change the constants in `main.py` to your need, then run the script. The output will be put in the `./output` folder.

---



#### Special Thank:

The CEO of a certain game company and [RazTools/Studio](https://gitlab.com/RazTools/Studio)
