#!/usr/bin/env python
from __future__ import print_function

import gnip_insights as insights
import json
import time
import requests

if __name__ == "__main__":
	consumer_key="CONSUMER_KEY_HERE"
	consumer_secret="CONSUMER_SECRET_HERE"
	token="TOKEN_HERE"
	token_secret="TOKEN_SECRET_HERE"

	TwentyEight_Hour_Flag = True
	Historical_Flag = True
	Totals_Flag = True

	# Filename of row delimited Tweet IDs
	TWEET_ID_FILENAME="tweet_ids.txt"

	engage=insights.Engagement(consumer_key, consumer_secret, token, token_secret)

	GROUP_BY_ENGAGEMENT_TYPE = {"engagement-grouping": { "group_by": [ "engagement.type", "tweet.id" ]}}

	tweet_ids=[]
	
	try:
		with open(TWEET_ID_FILENAME) as tweet_id_file:
			for tweet_id in tweet_id_file:
				tweet_ids.append(tweet_id)
	except IOError:
		print("  Error - Cannot find or open:", TWEET_ID_FILENAME)
	
	if len(tweet_ids) > 0:
	
		if TwentyEight_Hour_Flag:
			engage_28hr_response = engage.get_28hr(tweet_ids, GROUP_BY_ENGAGEMENT_TYPE )
			if engage_28hr_response.status_code == requests.codes.ok:
				print ("28 Hours:")
				print(json.dumps(engage_28hr_response.json(), indent=3))
			elif engage_28hr_response.status_code == requests.codes.unauthorized:
				print("28 Hours - Unauthorized Error")
			else:
				print("28 Hours - Error:",engage_28hr_response.status_code)
		
		if Historical_Flag:
			engage_historical_response = engage.get_historical(tweet_ids)
			if engage_historical_response.status_code == requests.codes.ok:
				print ("Historical:")
				print(json.dumps(engage_historical_response.json(), indent=3 ))
			elif engage_historical_response.status_code == requests.codes.unauthorized:
				print("Engagement Historical - Unauthorized Error")
			else:
				print("Engagement Historical - Error:", engage_historical_response.status_code)
		
		if Totals_Flag:
			engage_totals_response = engage.get_totals(tweet_ids)
			if engage_totals_response.status_code == requests.codes.ok:
				print("Totals:")
				print(json.dumps(engage_totals_response.json(), indent=3))
			elif engage_totals_response.status_code == requests.codes.unauthorized:
				print("Enagement Totals - Unauthorized Error")
			else:
				print("Enagement Totals - Error:",engage_totals_response.status_code)
