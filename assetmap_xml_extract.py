import os
import subprocess

# CONSTANTS

PATH_TO_HOYOSTUDIO = "D:\Codes\paimoooon\HoYoStudio 0.18.60\AssetStudioCLI.exe"
GAME = "BH3"            # --game <BH3|CB1|CB2|CB3|GI|SR|TOT|ZZZ> (REQUIRED)       Specify Game.

OLD_CLIENT = "E:\BH3 Beta\BH3_v6.5.14_0d50496ed892\BH3_Data\StreamingAssets\Asb\pc"
NEW_CLIENT = "E:\BH3 Beta\BH3_v6.6.14_ec783f1015c7\BH3_Data\StreamingAssets\Asb\pc"

OUTPUT_PATH = os.path.abspath("./input/")

# FUNCTIONS

def run_hoyostudio(input_path, map_name):
    args = [PATH_TO_HOYOSTUDIO,input_path,OUTPUT_PATH,'--game',GAME,"--map_op","AssetMap","--map_type","XML","--map_name",map_name]
    subprocess.run(args)

def assetmap_extract(old_client, new_client):
    print("Building AssetMap of the old client...")
    run_hoyostudio(old_client, "old_assetmap")

    print("Building AssetMap of the new client...")
    run_hoyostudio(new_client, "new_assetmap")

if __name__ == "__main__":

    assetmap_extract(OLD_CLIENT,NEW_CLIENT)
