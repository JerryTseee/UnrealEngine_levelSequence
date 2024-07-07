import unreal
import json
import os
import tkinter as tk
from tkinter import filedialog

def get_sequencer_objects():
	world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
	sequence_asset = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
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

def mgMetaHuman_face_keys_export():
	system_lib = unreal.SystemLibrary()
	root = tk.Tk()
	root.withdraw()

	face_anim = {}

	world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()

	sequence_asset, sequencer_objects_list,sequencer_names_list = get_sequencer_objects()
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
			keys_file = filedialog.asksaveasfile(initialfile = str(editor_asset_name) + '_' + character_name + '_face_anim' + '.json', defaultextension=".json",filetypes=[("All Files","*.*"),("JSON file","*.json")])

			keys_file.write('anim_keys_dict = ')
			keys_file.write(json.dumps(face_anim))
			print('Face Animation Keys output to: ' + str(keys_file.name))
		else:
			print(editor_asset_name)
			print('is not a level sequence. Skipping.')

mgMetaHuman_face_keys_export()