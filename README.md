# Python scripts for working with [Gnip](http://www.gnip.com) Audience and Engagement APIs
See:  the Support web site sections on [Audience API](http://support.gnip.com/apis/audience_api/) and [Engagement API](http://support.gnip.com/apis/engagement_api/) for more information.
###Note: Requires [Requests](http://docs.python-requests.org/en/master/) and [Requests-OAuthlib](https://requests-oauthlib.readthedocs.io/en/latest/) libraries.
To install: 
`pip install requests requests_oauthlib`
##gnip_insights.py
Library used to access Audience and Engagement APIs
##AudienceAPI.py
Sample app that uses all functions of Audience API.  Execute ./AudienceAPI.py to get show usage help:

![Audience API Demo Pic](https://github.com/GnipDz/Python-Insights/blob/master/AudienceAPI.jpg "Sample usage of app")


##gnip\_engagement\_test.py
Sample app to demonstrate retrieving engagement data for owned and authorized Tweets.  (improvements to come!)

##ConfigFile.py
Library used to manage reading/writing to gnip.cfg file where credentials are stored.

---
###Feedback
Please send help requests / comments / complaints / chocolate to [@SteveDz](stevedz@twitter.com)

Note that this code is provide "As Is".  You should review and understand Python code, and be able to debug this code _on your own_ if used in a production environment.  See the License file for more legal limitations.
