import os
import subprocess
import xml.sax
from tqdm import tqdm

from compare_xml import compare_xml_files

# CONSTANTS

OLD_XML = "./input/old_assetmap.xml"
NEW_XML = "./input/new_assetmap.xml"
OUTPUT_XML = "./output/added_assets.xml"

PATH_TO_HOYOSTUDIO = "D:\Codes\paimoooon\HoYoStudio 0.80.60\AssetStudioCLI.exe"
GAME = "BH3"            # --game <BH3|CB1|CB2|CB3|GI|SR|TOT|ZZZ> (REQUIRED)       Specify Game.
TYPE = "Texture2D"      # --type <Texture2D|Sprite|etc..>                         Specify unity class type(s)

ADDED_ASSETS = os.path.abspath("./output/added_assets.xml")
OUTPUT_PATH = os.path.abspath("./output/")
# CLASSES

class Handler(xml.sax.ContentHandler):
    def __init__(self, type):
        self.type = type
        self.buffer = None
        self.asset_list = []
        self.in_asset = False
        self.write_flag = False
        self.asset = ["",""]

    def startElement(self, name, attrs):
        if name == "Asset":
            self.write_flag = False
            self.in_asset = True
            self.asset = ["",""]
        elif self.in_asset:
            self.buffer = ""

    def endElement(self, name):
        if name == "Asset":
            self.in_asset = False
            if self.write_flag:
                self.asset_list.append(self.asset)
        elif name == "Name":
            self.asset[1] = self.buffer
            self.buffer = None
        elif name == "Type":
            if self.type == self.buffer:
                self.write_flag = True
            elif self.type != self.buffer:
                self.write_flag = False
            self.buffer = None
        elif name == "Source":
            self.asset[0] = self.buffer
            self.buffer = None
        elif self.in_asset:
            self.buffer = None

    def characters(self, content):
        if self.buffer is not None:
            self.buffer += content

def extraction_list_from_xml(added_assets, type):
    print("Converting XML to the extraction list...")
    parser = xml.sax.make_parser()
    handler = Handler(type)
    parser.setContentHandler(handler)
    parser.parse(added_assets)

    return handler.asset_list

def run_hoyostudio(input_path, reg):
    args = [PATH_TO_HOYOSTUDIO,input_path,OUTPUT_PATH,"--silent","--types",TYPE,"--names",reg,'--game',GAME]
    subprocess.run(args)

if __name__ == '__main__':

    compare_xml_files(OLD_XML, NEW_XML, OUTPUT_XML)
    
    extract_list = extraction_list_from_xml(ADDED_ASSETS, TYPE)

    print("Extracting...")
    for (file, asset) in tqdm(extract_list):
        run_hoyostudio(file, asset)
    
    print("Finished!")