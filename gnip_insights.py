import requests
from requests_oauthlib import OAuth1
import json
import sys

class Insights:
    """Gnip Insights API Client"""
    base_url = "https://data-api.twitter.com/insights/"
    json_header = {"Content-Type": "application/json"}

    def __init__(self, consumer_key, consumer_secret, token, token_secret):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._token = token
        self._token_secret = token_secret

    def get_auth(self):
        return OAuth1(self._consumer_key, self._consumer_secret, self._token, self._token_secret)


class Engagement(Insights):
    """Gnip Engagement API Client"""
    engagement_28hr_historical_json_encoded = json.loads(
        '{ "engagement_types": ["impressions", "engagements", "favorites", "replies", "retweets", "url_clicks", '
        '"hashtag_clicks", "detail_expands", "permalink_clicks", "media_clicks", "app_install_attempts", '
        '"user_follows", "user_profile_clicks", "video_views" ]}')
    engagement_totals_json_encoded = json.loads('{ "engagement_types": ["retweets", "favorites", "replies"]}')

    DEFAULT_GROUPING = {"by-tweet-id": {"group_by": ["tweet.id", "engagement.type"]}}

    def __init__(self, consumer_key, consumer_secret, token, token_secret):
        Insights.__init__(self, consumer_key, consumer_secret, token, token_secret)

    def get_28hr(self, tweets, groupings=DEFAULT_GROUPING):
        """Get 28 Hour Engagement data.  Pass in set of Tweet IDs"""

        request_json = self.engagement_28hr_historical_json_encoded.copy()
        request_json["tweet_ids"] = tweets

        if groupings is not None:
            request_json['groupings'] = groupings

        post_request = requests.post(Insights.base_url + "engagement/28hr",
                                     auth=Insights.get_auth(self),
                                     headers=Insights.json_header,
                                     data=json.dumps(request_json)
                                     )
        return post_request

    def get_historical(self, tweets, from_date=None, to_date=None, groupings=DEFAULT_GROUPING):
        """Get Historical Engagement data.  Pass in set of Tweet IDs"""
        request_json = Engagement.engagement_28hr_historical_json_encoded
        request_json["tweet_ids"] = tweets
        if from_date is not None:
            request_json['start'] = from_date

        if to_date is not None:
            request_json['end'] = to_date

        if groupings is not None:
            request_json['groupings'] = groupings

        post_request = requests.post(Insights.base_url + "engagement/historical",
                                     auth=Insights.get_auth(self),
                                     headers=Insights.json_header,
                                     data=json.dumps(request_json)
                                     )
        return post_request

    def get_totals(self, tweets, groupings=DEFAULT_GROUPING):
        """Get Totals Engagement data.  Pass in set of Tweet IDs"""

        request_json = self.engagement_totals_json_encoded.copy()
        request_json["tweet_ids"] = tweets

        if groupings is not None:
            request_json['groupings'] = groupings

        post_request = requests.post(Insights.base_url + "engagement/totals",
                                     auth=Insights.get_auth(self),
                                     headers=Insights.json_header,
                                     data=json.dumps(request_json)
                                     )
        return post_request


class Audience(Insights):
    """Gnip Audience API Client"""

    def __init__(self, consumer_key, consumer_secret, token, token_secret):
        Insights.__init__(self, consumer_key, consumer_secret, token, token_secret)

    def create_segment(self, name):
        """Segment Create - Pass in a text name"""
        request_json = json.loads("{\"name\": \"" + name + "\"}")
        post_request = requests.post(Insights.base_url + "audience/segments",
                                     auth=Insights.get_auth(self),
                                     headers=Insights.json_header,
                                     data=json.dumps(request_json)
                                     )
        return post_request

    def get_segments(self):
        """Get All Segments - no parameters passed"""
        get_request = requests.get(Insights.base_url + "audience/segments",
                                   auth=Insights.get_auth(self),
                                   headers=Insights.json_header
                                   )
        return get_request

    def get_segment(self, segment_id):
        """Get Segments - pass in by id"""
        get_request = requests.get(Insights.base_url + "audience/segments/" + segment_id,
                                   auth=Insights.get_auth(self),
                                   headers=Insights.json_header
                                   )
        return get_request

    def append_to_segment(self, segment_id, id_list):
        """Append User IDs to Segment.  Pass in segment ID and list of ID"""
        user_ids = {"user_ids": []}
        user_ids['user_ids'].extend(id_list)
        post_request = requests.post(Insights.base_url + "audience/segments/" + segment_id + "/ids",
                                     auth=Insights.get_auth(self),
                                     headers=Insights.json_header,
                                     data=json.dumps(user_ids)
                                     )
        return post_request

    def create_segment_from_followers(self, segment_name, id_list):
        """Create Segment from followers of user IDs.  Pass in segment name and list of IDs"""
        post_data = {"name": segment_name, "followed": {"user_ids": id_list}}
        post_request = requests.post(Insights.base_url + "audience/segments",
                                     auth=Insights.get_auth(self),
                                     headers=Insights.json_header,
                                     data=json.dumps(post_data)
                                     )
        return post_request

    def create_segment_from_impressed(self, segment_name, id_list):
        """Create Segment from users who viewed with Tweets from user IDs.  Pass in segment name and list of IDs"""
        post_data = {"name": segment_name, "impressed": {"user_ids": id_list}}
        post_request = requests.post(Insights.base_url + "audience/segments",
                                     auth=Insights.get_auth(self),
                                     headers=Insights.json_header,
                                     data=json.dumps(post_data)
                                     )
        return post_request

    def create_segment_from_engaged(self, segment_name, id_list):
        """Create Segment from users who engaged with Tweets from user IDs.  Pass in segment name and list of IDs"""
        post_data = {"name": segment_name, "engaged": {"user_ids": id_list}}
        post_request = requests.post(Insights.base_url + "audience/segments",
                                     auth=Insights.get_auth(self),
                                     headers=Insights.json_header,
                                     data=json.dumps(post_data)
                                     )
        return post_request

    def create_segment_from_tailored(self, segment_name, id_list):
        """Create Segment from users who engaged with Tweets from user IDs.  Pass in segment name and list of IDs"""
        post_data = {"name": segment_name, "tailored": {"tailored_audience_ids": id_list}}
        post_request = requests.post(Insights.base_url + "audience/segments",
                                     auth=Insights.get_auth(self),
                                     headers=Insights.json_header,
                                     data=json.dumps(post_data)
                                     )
        return post_request

    def delete_segment(self, segment_id):
        """Delete existing Segment.  Pass in segment ID"""
        delete_request = requests.delete(Insights.base_url + "audience/segments/" + segment_id,
                                         auth=Insights.get_auth(self),
                                         headers=Insights.json_header
                                         )
        return delete_request

    def create_audience(self, name, segment_ids):
        """Segment Create - Pass in a text name and list of segments"""
        request_json = json.loads("{\"name\": \"" + name + "\"}")
        request_json['segment_ids'] = segment_ids

        post_request = requests.post(Insights.base_url + "audience/audiences",
                                     auth=Insights.get_auth(self),
                                     headers=Insights.json_header,
                                     data=json.dumps(request_json)
                                     )
        return post_request

    def get_audiences(self):
        """Get All Audiences - no parameters passed"""
        get_request = requests.get(Insights.base_url + "audience/audiences",
                                   auth=Insights.get_auth(self),
                                   headers=Insights.json_header
                                   )
        return get_request

    def delete_audience(self, audience_id):
        """Delete existing Audience.  Pass in audience ID"""
        delete_request = requests.delete(Insights.base_url + "audience/audiences/" + audience_id,
                                         auth=Insights.get_auth(self),
                                         headers=Insights.json_header
                                         )
        return delete_request

    def get_audience_query(self, audience_id, groupings):
        """Query audience for insights.  Pass in audience id and groupings JSON"""
        request_json = groupings

        post_request = requests.post(Insights.base_url + "audience/audiences/" + audience_id + "/query",
                                     auth=Insights.get_auth(self),
                                     headers=Insights.json_header,
                                     data=json.dumps(request_json)
                                     )
        return post_request

    def get_usage(self):
        """Get usage statistics - no parameters passed"""
        get_request = requests.get(Insights.base_url + "audience/usage",
                                   auth=Insights.get_auth(self),
                                   headers=Insights.json_header
                                   )
        return get_request
