# Python scripts for working with [Gnip](www.gnip.com) Audience and Engagement APIs
See:  the Support web site sections on [Audience API](http://support.gnip.com/apis/audience_api/) and [Engagement API](http://support.gnip.com/apis/engagement_api/) for more information.
###Note: Requires [Requests](http://docs.python-requests.org/en/master/) library - to install: 
`pip install requests`
##gnip_insights.py
Library used to access Audience and Engagement APIs
##AudienceAPI.py
Sample app that uses all functions of Audience API.  Execute ./AudienceAPI.py to get show usage help:

```
./AudienceAPI.py ACTION [ parameters ]
./AudienceAPI.py set-access-token ACCESS_TOKEN
./AudienceAPI.py set-access-token-secret ACCESS_TOKEN_SECRET
./AudienceAPI.py set-consumer-key CONSUMER_KEY
./AudienceAPI.py set-consumer-secret CONSUMER_SECRET
./AudienceAPI.py create-followed-segment SEGMENT_NAME USER_ID
./AudienceAPI.py create-engagement-segment SEGMENT_NAME USER_ID
./AudienceAPI.py create-impressed-segment SEGMENT_NAME USER_ID
./AudienceAPI.py create-tailored-segment SEGMENT_NAME
./AudienceAPI.py create-segment SEGMENT_NAME
./AudienceAPI.py append-segment SEGMENT_NAME USERID_FILENAME.CSV
./AudienceAPI.py create-audience AUDIENCE_NAME SEGMENT_NAME SEGMENT_NAME ...
./AudienceAPI.py query-audience AUDIENCE_NAME GROUPING_NAME_1 GROUPING_NAME_2 ... (up to 10 groupings) 
./AudienceAPI.py delete-audience AUDIENCE_NAME
./AudienceAPI.py delete-segment SEGMENT_NAME
./AudienceAPI.py list-audiences
./AudienceAPI.py list-segments
./AudienceAPI.py list-groupings
./AudienceAPI.py usage
```

##gnip\_engagement\_test.py
Sample app to demonstrate retrieving engagement data for owned and authorized Tweets.  (improvements to come!)

##ConfigFile.py
Library used to manage reading/writing to gnip.cfg file where credentials are stored.

---
###Feedback
Please send help requests / comments / complaints / chocolate to [@SteveDz](stevedz@twitter.com)

Note that this code is provide "As Is".  You should review and understand Python code, and be able to debug this code _on your own_ if used in a production environment.  See the License file for more legal limitations.
