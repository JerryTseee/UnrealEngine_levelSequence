"""
Here using the file "20240504_006Vasilisa_32" as an example;
the video fps is 60, and frames is 4580;
(UE default is 30 fps, so we need to get the frame number and convert it!)
"""
import unreal
import json


#First Step: add a new level sequence
# Get asset tools
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
# Create a Level Sequence with name LevelSequenceName in root content folder
level_sequence = unreal.AssetTools.create_asset(asset_tools, asset_name = "LevelSequenceName", package_path = "/Game/", asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())



#Second Step: get and change the frame range
json_file_path = "E:\\ARFriendInteract\\Captures\\iPhoneSpeech\\20240504_006Vasilisa_32\\take.json"

with open(json_file_path) as file:
    data = json.load(file)

frames_value = data["frames"]
value = frames_value // 2

level_sequence.set_playback_start(0)#starting frame will always be 0
level_sequence.set_playback_end(value)#end