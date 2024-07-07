import unreal
#First Step: add a new level sequence
# Get asset tools
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
# Create a Level Sequence with name LevelSequenceName in root content folder
level_sequence = unreal.AssetTools.create_asset(asset_tools, asset_name = "LevelSequenceName", package_path = "/Game/", asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())

#Second Step: change the frame range
# Set the playback range
level_sequence.set_playback_start(0)
level_sequence.set_playback_end(2000)

#Third Step: add a character: Cooper!
# Load the character asset
character_asset_path = "/Game/MetaHumans/Cooper/BP_Cooper"
character_asset = unreal.EditorAssetLibrary.load_asset(character_asset_path)
# Add the character to the level sequence
level_sequence.add_possessable(character_asset)

# Optionally, you can set the character's transform (position, rotation, scale) within the sequence:
#character_possessable = level_sequence.find_possessable(character_asset)
#character_possessable.set_transform(unreal.Transform())
