# Introduction  
This Python script interacts with Unreal Engine using the Unreal Python API to automate certain actions within the Unreal Engine Editor. The script adds a new actor to the world, reads JSON files in a specified folder, creates a new level sequence based on the JSON data, and adds the actor to the level sequence. Then add the animation sequence to the face of the actor, bake the control rig of the face, and then output the animation sequence key json file.  
# Flow Explanation  
The first step is to create a new metahuman actor (here is Cooper), then create a dictionary as an indicator to the folder contains animation sequences. Then for each animation sequence, start to process the current one. Firstly, create a new level sequence, then create the animation track for the actor and actor's face; load the current animation sequence into the face. Finally, bake the control rig to the face, and export to the destination folder.
# Example  
<img width="479" alt="image" src="https://github.com/JerryTseee/UnrealEngine_levelSequence/assets/126223772/501b460c-94a2-4074-bd6f-8563e42ae0d4">
<img width="195" alt="image" src="https://github.com/JerryTseee/UnrealEngine_levelSequence/assets/126223772/a11eeaca-271a-48f8-b28c-87225e75adad">
