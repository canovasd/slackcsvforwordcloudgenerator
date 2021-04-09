import os
import json
import logging
import collections
from time import sleep

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

forbiddenWords = ["para", "entrou", "canal", "teve", "como", "então", "isso", "esse", "este", "está", "estão", "estao"]


# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token="YOUR_TOKEN_HERE")
# Store conversation history
conversation_history = []

oldest = "1577898098.003500" #jan 2020


wordMap = {"user": {"user": 0}}

def extractWords(channel_id: str, nextCursor: str):

	try:
	    # Call the conversations.history method using the WebClient
	    # conversations.history returns the first 100 messages by default
	    # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination

	    if nextCursor != "":
	    	result = client.conversations_history(channel=channel_id, limit=1000, oldest = oldest)
	    else:
	    	result = client.conversations_history(channel=channel_id, limit=1000, cursor = nextCursor, oldest = oldest)

	    conversation_history = result["messages"]

	    for conversation in conversation_history:
	    	if("user" in conversation and "text" in conversation):
	    	    user = conversation["user"]
	    	    text = conversation["text"]
	    	    if(not user in wordMap):
	    	    	wordMap.update({user: {}})
			    
	    	    for word in text.replace(",", "").replace(".","").replace(":", "").lower().split():
	    	    	if len(word) > 2: 
	    	    		if(not word in wordMap[user]):
			    	    	wordMap[user].update({word: 0})
	    	    		wordMap[user][word] = wordMap[user][word] + 1


	    #print("{} messages found in {}".format(len(conversation_history), id))

	    #if(result["response_metadata"]):
	    	#sleep(1)
	    	#print("page")
	    	#extractWords(channel_id, result["response_metadata"]["next_cursor"])

	except SlackApiError as e:
	    print("Error creating conversation: {}".format(e))


extractWords("CKUKFMFAS", "") #geral
extractWords("C01FYQPHBPE", "") #planeta
extractWords("C01HVJ838FJ", "") #agendamentos
extractWords("CP86MQHSS", "") #dev
extractWords("CQEGV71FW", "") #front
extractWords("CQJKAUC8P", "") #payments
extractWords("CT5HV5PGS", "") #perolas
extractWords("CPV9S3VB9", "") #product
extractWords("CMVT0QKGE", "") #random
extractWords("C01JN4KRFMW", "") #squad-chronos
extractWords("C01FMCTM91C", "") #squad-ops-experience
extractWords("C01CY2J1EH3", "") #squad-vendas
extractWords("CQJ06K69Z", "") #theia-news
extractWords("C01CT7K69U4", "") #toda-theia
extractWords("C01FC0NK9PH", "") #squad-growth
extractWords("C01SJCCSV09", "") #linkdadaily
extractWords("CQ7BKRG4S", "") #bugs
extractWords("C01BKNLM11C", "") #time-social
extractWords("C0109FHRHPA", "") #ajudacomcliente
extractWords("C01G1J1URPC", "") #design
extractWords("C01H0TQEL4R", "") #kits

for key, val in wordMap.items():
	for word, counter in val.items():
		if counter > 0 and word not in forbiddenWords:
    			print('{};{};{}'.format(key, word , counter))
