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



animation_sequence = dict()
#assume the dataset is only 50 folders !!! (important, need to be changed base on real dataset number)
for i in range(2,50):
    animation_sequence[i] = False



path = "F:\\Jerry\\Vasilisa" #folder that contain all the character folders

#for every character folder, start to do the work:
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




            #start to load into the animation to the current face track:
            #assuming that the name of the animation sequence is "AS_va + number"
            face_anim_path = "/Game/MetaHumans/AS_va"
            #then from low to high to load the animation sequence into the current face track (if the sequenced is loaded before, it will not be loaded again, then go the next)
            for i in range(2,50):
                final_face_anim_path = face_anim_path + str(i)
                if final_face_anim_path:#if the path exists
                    if animation_sequence[i] == False:#if the animation sequence is not used before
                        animation_sequence[i] = True
                        anim_asset = unreal.EditorAssetLibrary.load_asset(final_face_anim_path)
                        print("animation sequence:")
                        print(anim_asset)
                        break
                else:
                    continue
            anim_asset = unreal.AnimSequence.cast(anim_asset)
            params = unreal.MovieSceneSkeletalAnimationParams()
            params.set_editor_property("Animation", anim_asset)


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




        
            #add face animation track
            components = new_actor.get_components_by_class(unreal.SkeletalMeshComponent)
            print("Components of Cooper: ")
            print(components)

            face_component = None
            for component in components:
                if component.get_name() == "Face":
                    face_component = component
                    break
            print(face_component)

            #get the face track (same technique as above):
            face_binding = level_sequence.add_possessable(face_component)
            print(face_binding)
            transform_track2 = face_binding.add_track(unreal.MovieScene3DTransformTrack)
            anim_track2 = face_binding.add_track(unreal.MovieSceneSkeletalAnimationTrack)
            transform_section2 = transform_track2.add_section()
            anim_section2 = anim_track2.add_section()
            anim_section2.set_editor_property("Params", params)#add animation
            transform_section2.set_range(start_frame, end_frame)
            anim_section2.set_range(start_frame, end_frame)
            



		    # Refresh to visually see the new tracks and sections added
            unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

print("Done!")