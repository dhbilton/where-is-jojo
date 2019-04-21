'''
================================================================================
||        	                 					  							  ||
||                  	    		RESPONSE		  					  	  ||
||          	               					  							  ||
================================================================================
This file contains code that creates an approrpiate response from the given
input

@author: Janak A Jain

'''

import json
import pandas as pd
import time
from load import *


with open('data/messages.json') as messages_data:
	messages = json.load(messages_data)[0]  # This is a dictionary of messages 

with open('data/stories.json') as stories_data:
	stories = json.load(stories_data)[0]  # This is a dictionary of stories



input_keys = ["timestamp","user_id","session_id","tags",\
"return_targets","return_intent","text","embed"]

user_keys = ["name","age","sex","phone"]

# intent = []
# targets = []
entities = []
resp_text = []


def respond(intent = None, targets = None, entities = None, user = None, \
	type = None, title = None, text = None, embed_key=None):

	print('Incoming input to response: ')
	print("Intent = " +str(intent))
	print("Targets = " +str(targets))
	print("Entities = " +str(entities))
	print(" User = " + str(user))

	resp = dict.fromkeys(input_keys)

	if(type == "message"):

		intent_m = []
		targets_m = []

		print(messages.keys())


		for i in messages.keys():
			m = messages[i]
			if any(i in m["intent"] for i in intent):
				intent_m.append(m)
				# intent = set(intent + m["intent"])

		# for m in intent_m:
			if any(t in m["targets"] for t in targets):
				if("leadgen" not in m["intent"]):
					targets_m.append(m)
				# targets = set(targets.append(m["targets"]))

		print("Intents messages = " + str(intent_m))
		print()
		print("Targets messages = " + str(targets_m))

		if(len(targets_m) > 0):
			# Select the best message

			message = targets_m[0]
		else:
			message = targets_m

		resp_text = []

		resp_text.append(message["text"])

		if(embed_key != None):
			resp_text.append('\n'.join(user[embed_key]))



		resp["user_id"] = user["phone"]
		resp["session_id"] = 1           # TODO - change this later
		# resp["return_tags"] = list(set(intent + [t for t in targets]))
		resp["return_tags"] = []
		resp["return_intent"] = intent
		resp["return_targets"] = targets
		resp["text"] = resp_text
		resp["timestamp"] = time.time()
		resp["embed"] = message["embed"]

		print("Response in message logic: ")
		print(resp)




	elif(type == "story"):
		for s_name in stories.keys():
			
			# print("     Testing story: " + s_name)

			story = stories[s_name]

			# print("     Comparison = " + str(sorted(story["targets"]) == sorted(targets)))

			if(len(targets) >0):

				resp_text = []

				if(sorted(story["targets"]) == sorted(targets)):

					print("     Serving story: " + s_name)

					for m_id in story["messages"]:

						resp_text.append(messages[str(m_id)]["text"])
					
					intent = story["return_intent"]
					targets = story["return_targets"]
					embed = messages[str(m_id)]["embed"]

					intent = list(set(intent))
					targets = list(set(targets))


					resp["user_id"] = user["phone"]
					resp["session_id"] = 1           # TODO - change this later
					resp["return_tags"] = list(set(intent + [t for t in targets]))
					resp["return_intent"] = intent
					resp["return_targets"] = targets
					resp["text"] = resp_text
					resp["timestamp"] = time.time()
					resp["embed"] = embed

					# Reset intents, targets and tags

					intent = []
					targets = []
					entities = []
					resp_text = []

				# elif(any(t in targets for t in story["targets"])):

				# 	# Include a filtering function here

				# 	print("     Serving story: " + s_name)

				# 	for m_id in story["messages"]:

				# 		resp_text.append(messages[str(m_id)]["text"])
					
				# 	intent = story["return_intent"]
				# 	targets = story["return_targets"]
				# 	embed = messages[str(m_id)]["embed"]

				# 	intent = list(set(intent))
				# 	targets = list(set(targets))


				# 	resp["user_id"] = user["phone"]
				# 	resp["session_id"] = 1           # TODO - change this later
				# 	resp["return_tags"] = list(set(intent + [t for t in targets]))
				# 	resp["return_intent"] = intent
				# 	resp["return_targets"] = targets
				# 	resp["text"] = resp_text
				# 	resp["timestamp"] = time.time()
				# 	resp["embed"] = embed

				# 	# Reset intents, targets and tags

				# 	intent = []
				# 	targets = []
				# 	entities = []
				# 	resp_text = []

	elif(type == "symptom"):
		
		print("Symptom loop")

		resp["user_id"] = user["phone"]
		resp["session_id"] = 1           # TODO - change this later
		resp["return_tags"] = []
		resp["return_intent"] = intent
		resp["return_targets"] = targets
		resp["text"] = text
		resp["timestamp"] = time.time()
		resp["embed"] = []



		









	else:
		resp["text"] = "No match"
		resp["embed"] = []
		
	
	return resp
