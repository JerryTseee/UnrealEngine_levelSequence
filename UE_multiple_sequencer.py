import unreal
import json
import os

"""
(UE default is 30 fps, so we need to get the frame number and convert it!)
"""

# add a new actor into the world
actor_path = "/Game/MetaHumans/Cooper/BP_Cooper"
actor_class = unreal.EditorAssetLibrary.load_blueprint_class(actor_path)
coordinate = unreal.Vector(-25200.0, -25200.0, 100.0)
editor_subsystem = unreal.EditorActorSubsystem()
new_actor = editor_subsystem.spawn_actor_from_class(actor_class, coordinate)



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

            asset_name = set_path.split("\\")[-1] #get the last part of the path

            level_sequence = unreal.AssetTools.create_asset(asset_tools, asset_name, package_path = "/Game/", asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())
            
            level_sequence.set_playback_start(0) #starting frame will always be 0
            
            level_sequence.set_playback_end(value) #end




            #add the actor into the level sequence
            actor_binding = level_sequence.add_possessable(new_actor)

            transform_track = actor_binding.add_track(unreal.MovieScene3DTransformTrack)
            anim_track = actor_binding.add_track(unreal.MovieSceneSkeletalAnimationTrack)

		    # Add section to track to be able to manipulate range, parameters, or properties
            transform_section = transform_track.add_section()
            anim_section = anim_track.add_section()

		    # Get level sequence start and end frame
            start_frame = level_sequence.get_playback_start()
            end_frame = level_sequence.get_playback_end()

		    # Set section range to level sequence start and end frame
            transform_section.set_range(start_frame, end_frame)
            anim_section.set_range(start_frame, end_frame)

		    # Refresh to visually see the new tracks and sections added
            unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

print("Done!")