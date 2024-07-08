import unreal
import json
import os

"""
(UE default is 30 fps, so we need to get the frame number and convert it!)
"""

path = "F:\\Jerry\\Vasilisa" #folder that contain all the character folders

for i in os.listdir(path):
    set_path = os.path.join(path, i) #the path of each specific character folder
    if os.path.isdir(set_path):
        #if it is indeed a directory
        json_file_path = os.path.join(set_path, "take.json")
        if os.path.isfile(json_file_path):
            #if the json file exists -> create a new level sequence -> set the playback range
            with open(json_file_path) as file:
                data = json.load(file)
                
            frames_value = data["frames"]
            value = frames_value // 2 #this is the upper bound of the frame range

            #create a new level sequence
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

            #name the asset_name:
            asset_name = set_path.split("\\")[-1] #get the last part of the path

            level_sequence = unreal.AssetTools.create_asset(asset_tools, asset_name, package_path = "/Game/", asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())
            
            level_sequence.set_playback_start(0) #starting frame will always be 0
            
            level_sequence.set_playback_end(value) #end