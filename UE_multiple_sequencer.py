import unreal
import json
import os
import tkinter as tk
from tkinter import filedialog


# function to get the current level sequence and the sequencer objects
def get_sequencer_objects(level_sequence):
	world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
	#sequence_asset = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
	sequence_asset = level_sequence
	range = sequence_asset.get_playback_range()
	sequencer_objects_list = []
	sequencer_names_list = []
	bound_objects = []

	sequencer_objects_list_temp = unreal.SequencerTools.get_bound_objects(world, sequence_asset, sequence_asset.get_bindings(), range)

	for obj in sequencer_objects_list_temp:
		bound_objects = obj.bound_objects

		if len(bound_objects)>0:
			if type(bound_objects[0]) == unreal.Actor:
				sequencer_objects_list.append(bound_objects[0])
				sequencer_names_list.append(bound_objects[0].get_actor_label())
	return sequence_asset, sequencer_objects_list, sequencer_names_list


# function to export the face animation keys to a json file
def mgMetaHuman_face_keys_export(level_sequence, output_path):
	system_lib = unreal.SystemLibrary()
	root = tk.Tk()
	root.withdraw()

	face_anim = {}

	world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()

	sequence_asset, sequencer_objects_list,sequencer_names_list = get_sequencer_objects(level_sequence)
	face_possessable = None

	editor_asset_name = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(sequence_asset).split('.')[-1]
	
	for num in range(0, len(sequencer_names_list)):
		actor = sequencer_objects_list[num]
		asset_name = actor.get_actor_label()
		bp_possessable = sequence_asset.add_possessable(actor)
		child_possessable_list = bp_possessable.get_child_possessables()
		character_name = ''

		for current_child in child_possessable_list:
			if 'Face' in current_child.get_name():
				face_possessable = current_child
		
		if face_possessable:
			character_name = (face_possessable.get_parent().get_display_name())
			face_possessable_track_list = face_possessable.get_tracks()
			face_control_rig_track = face_possessable_track_list[len(face_possessable_track_list)-1]
			face_control_channel_list = unreal.MovieSceneSectionExtensions.get_all_channels(face_control_rig_track.get_sections()[0])
			face_control_name_list = []

			for channel in face_control_channel_list:
				channel_name = str(channel.get_name())
				channel_string_list = channel_name.split('_')
				channel_name = channel_name.replace('_' + channel_string_list[-1], '')
				face_control_name_list.append(channel_name)

			for ctrl_num in range(0, len(face_control_channel_list)):
				control_name = face_control_name_list[ctrl_num]

				try:
					numKeys = face_control_channel_list[ctrl_num].get_num_keys()
					key_list = [None] * numKeys
					keys = face_control_channel_list[ctrl_num].get_keys()
					for key in range(0, numKeys):
						key_value = keys[key].get_value()
						key_time = keys[key].get_time(time_unit=unreal.SequenceTimeUnit.DISPLAY_RATE).frame_number.value
						key_list[key]=([key_value, key_time])

					face_anim[control_name] = key_list
				except:
					face_anim[control_name] = []
			
			character_name = str(character_name)
			if 'BP_' in character_name:
				character_name = character_name.replace('BP_', '')
			if 'BP ' in character_name:
				character_name = character_name.replace('BP ', '')

			character_name = character_name.lower()
			print('character_name is ' + character_name)
            
			
			folder_path = output_path
			os.makedirs(folder_path, exist_ok=True)
			file_path = os.path.join(folder_path, f'{editor_asset_name}_{character_name}_face_anim.json')
			with open(file_path, 'w') as keys_file:
				keys_file.write('anim_keys_dict = ')
				keys_file.write(json.dumps(face_anim))
				
			
			
			print('Face Animation Keys output to: ' + str(keys_file.name))
		else:
			print(editor_asset_name)
			print('is not a level sequence. Skipping.')



# Below is the main steps:
"""
(UE default is 30 fps, so we need to get the frame number and convert it!)
"""

# add a new actor into the world
actor_path = "/Game/MetaHumans/Cooper/BP_Cooper" # the path of the actor
actor_class = unreal.EditorAssetLibrary.load_blueprint_class(actor_path)
coordinate = unreal.Vector(-25200.0, -25200.0, 100.0) # randomly put it on a coordinate of the world
editor_subsystem = unreal.EditorActorSubsystem()
new_actor = editor_subsystem.spawn_actor_from_class(actor_class, coordinate)



animation_sequence = dict()
#assume the dataset is only 50 folders !!! Important, need to be changed base on real dataset number!! And number order should be 1, 2, 3, 4, ... ...
for i in range(2,50):
    animation_sequence[i] = False



path = "F:\\Jerry\\Pipeline\\Vasilisa" #folder that contain all the character folders, need to be changed base on the real path

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
            value = frames_value // 2 + 1 #this is the upper bound of the frame range

            #create a new level sequence
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

            asset_name = set_path.split("\\")[-1] #get the last part of the path

            level_sequence = unreal.AssetTools.create_asset(asset_tools, asset_name, package_path = "/Game/", asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())
            
            level_sequence.set_playback_start(0) #starting frame will always be 0
            
            level_sequence.set_playback_end(value) #end



            #start to load into the animation to the current face track:
            #assuming that the name of the animation sequence is "AS_va + number" ! Need to be changed base on the real name
            face_anim_path = "/Game/MetaHumans/AS_va"
            #then from low to high to load the animation sequence into the current face track (if the sequenced is loaded before, it will not be loaded again, then go the next)
            for i in range(2,50):#And number order of the animation file should be 1, 2, 3, 4, ... ...
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
            
            
            # bake to control rig to the face
            print("level sequence: " + str(level_sequence))

            editor_subsystem = unreal.UnrealEditorSubsystem()
            world = editor_subsystem.get_editor_world()
            print("world: " + str(world))

            anim_seq_export_options = unreal.AnimSeqExportOption()
            print("anim_seq_export_options: " + str(anim_seq_export_options))

            control_rig = unreal.load_object(name = '/Game/MetaHumans/Common/Face/Face_ControlBoard_CtrlRig', outer = None)
            control_rig_class = control_rig.get_control_rig_class()# use class type in the under argument
            print("control rig class: " + str(control_rig_class))
            
            unreal.ControlRigSequencerLibrary.bake_to_control_rig(world, level_sequence, control_rig_class = control_rig_class, export_options = anim_seq_export_options, tolerance = 0.01, reduce_keys = False, binding = face_binding)


		    # Refresh to visually see the new level sequence
            unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()
			
            # Export the current face animation keys to a json file
            output_path = "F:\\Jerry\\Pipeline\\output_sequence"
            mgMetaHuman_face_keys_export(level_sequence, output_path)
            unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

print("Well Done! Jerry!")
