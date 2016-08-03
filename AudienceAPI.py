#!/usr/bin/env python
from __future__ import print_function

import gnip_insights as insights
import json
import requests
import ConfigFile
import sys
import datetime


def parameter_help():
    print(" ")
    print ("Usage:")
    print ("./AudienceAPI.py ACTION [ parameters ]")
    print ("./AudienceAPI.py set-access-token ACCESS_TOKEN")
    print ("./AudienceAPI.py set-access-token-secret ACCESS_TOKEN_SECRET")
    print ("./AudienceAPI.py set-consumer-key CONSUMER_KEY")
    print ("./AudienceAPI.py set-consumer-secret CONSUMER_SECRET")
    print ("./AudienceAPI.py create-segment SEGMENT_NAME")
    print ("./AudienceAPI.py create-followed-segment SEGMENT_NAME USER_ID")
    print ("./AudienceAPI.py create-engagement-segment SEGMENT_NAME USER_ID")
    print ("./AudienceAPI.py create-impressed-segment SEGMENT_NAME USER_ID")
    print ("./AudienceAPI.py create-tailored-segment SEGMENT_NAME")
    print ("./AudienceAPI.py create-segment SEGMENT_NAME")
    print ("./AudienceAPI.py append-segment SEGMENT_NAME USERID_FILENAME.CSV")
    print ("./AudienceAPI.py create-audience AUDIENCE_NAME SEGMENT_NAME SEGMENT_NAME ...")
    print ("./AudienceAPI.py query-audience AUDIENCE_NAME GROUPING_NAME_1 GROUPING_NAME_2 ... (up to 10 groupings) ")
    print ("./AudienceAPI.py delete-audience AUDIENCE_NAME")
    print ("./AudienceAPI.py delete-segment SEGMENT_NAME")
    print ("./AudienceAPI.py list-audiences")
    print ("./AudienceAPI.py list-segments")
    print ("./AudienceAPI.py list-groupings")
    print ("./AudienceAPI.py usage")


def arg_count_check(minimum):
    if (len(sys.argv) - 1) < minimum:
        parameter_help()
        sys.exit(2)


def get_audience_object():
    oauth = ConfigFile.get_settings("gnip.cfg", "oauth")
    audience = insights.Audience(oauth["consumerkey"], oauth["consumersecret"], oauth["token"], oauth["tokensecret"])
    return audience


def get_groupings():
    groupings = {
        "user-gender": {"group_by": ["user.gender"]},
        "user-language": {"group_by": ["user.language"]},
        "user-interest": {"group_by": ["user.interest"]},
        "user-tv-genre": {"group_by": ["user.tv.genre"]},
        "user-location-country": {"group_by": ["user.location.country"]},
        "user-location-region": {"group_by": ["user.location.region"]},
        "user-location-metro": {"group_by": ["user.location.metro"]},
        "user-device-os": {"group_by": ["user.device.os"]},
        "user-device-network": {"group_by": ["user.device.network"]},
        "user-gender-user-language": {"group_by": ["user.gender", "user.language"]},
        "user-gender-user-interest": {"group_by": ["user.gender", "user.interest"]},
        "user-gender-user-tv-genre": {"group_by": ["user.gender", "user.tv.genre"]},
        "user-gender-user-location-country": {"group_by": ["user.gender", "user.location.country"]},
        "user-gender-user-location-region": {"group_by": ["user.gender", "user.location.region"]},
        "user-gender-user-location-metro": {"group_by": ["user.gender", "user.location.metro"]},
        "user-gender-user-device-os": {"group_by": ["user.gender", "user.device.os"]},
        "user-gender-user-device-network": {"group_by": ["user.gender", "user.device.network"]},
        "user-language-user-gender": {"group_by": ["user.language", "user.gender"]},
        "user-language-user-interest": {"group_by": ["user.language", "user.interest"]},
        "user-language-user-tv-genre": {"group_by": ["user.language", "user.tv.genre"]},
        "user-language-user-location-country": {"group_by": ["user.language", "user.location.country"]},
        "user-language-user-location-region": {"group_by": ["user.language", "user.location.region"]},
        "user-language-user-location-metro": {"group_by": ["user.language", "user.location.metro"]},
        "user-language-user-device-os": {"group_by": ["user.language", "user.device.os"]},
        "user-language-user-device-network": {"group_by": ["user.language", "user.device.network"]},
        "user-interest-user-gender": {"group_by": ["user.interest", "user.gender"]},
        "user-interest-user-language": {"group_by": ["user.interest", "user.language"]},
        "user-interest-user-tv-genre": {"group_by": ["user.interest", "user.tv.genre"]},
        "user-interest-user-location-country": {"group_by": ["user.interest", "user.location.country"]},
        "user-interest-user-location-region": {"group_by": ["user.interest", "user.location.region"]},
        "user-interest-user-location-metro": {"group_by": ["user.interest", "user.location.metro"]},
        "user-interest-user-device-os": {"group_by": ["user.interest", "user.device.os"]},
        "user-interest-user-device-network": {"group_by": ["user.interest", "user.device.network"]},
        "user-tv-genre-user-gender": {"group_by": ["user.tv.genre", "user.gender"]},
        "user-tv-genre-user-language": {"group_by": ["user.tv.genre", "user.language"]},
        "user-tv-genre-user-interest": {"group_by": ["user.tv.genre", "user.interest"]},
        "user-tv-genre-user-location-country": {"group_by": ["user.tv.genre", "user.location.country"]},
        "user-tv-genre-user-location-region": {"group_by": ["user.tv.genre", "user.location.region"]},
        "user-tv-genre-user-location-metro": {"group_by": ["user.tv.genre", "user.location.metro"]},
        "user-tv-genre-user-device-os": {"group_by": ["user.tv.genre", "user.device.os"]},
        "user-tv-genre-user-device-network": {"group_by": ["user.tv.genre", "user.device.network"]},
        "user-location-country-user-gender": {"group_by": ["user.location.country", "user.gender"]},
        "user-location-country-user-language": {"group_by": ["user.location.country", "user.language"]},
        "user-location-country-user-interest": {"group_by": ["user.location.country", "user.interest"]},
        "user-location-country-user-tv-genre": {"group_by": ["user.location.country", "user.tv.genre"]},
        "user-location-country-user-location-region": {"group_by": ["user.location.country", "user.location.region"]},
        "user-location-country-user-location-metro": {"group_by": ["user.location.country", "user.location.metro"]},
        "user-location-country-user-device-os": {"group_by": ["user.location.country", "user.device.os"]},
        "user-location-country-user-device-network": {"group_by": ["user.location.country", "user.device.network"]},
        "user-location-region-user-gender": {"group_by": ["user.location.region", "user.gender"]},
        "user-location-region-user-language": {"group_by": ["user.location.region", "user.language"]},
        "user-location-region-user-interest": {"group_by": ["user.location.region", "user.interest"]},
        "user-location-region-user-tv-genre": {"group_by": ["user.location.region", "user.tv.genre"]},
        "user-location-region-user-location-country": {"group_by": ["user.location.region", "user.location.country"]},
        "user-location-region-user-location-metro": {"group_by": ["user.location.region", "user.location.metro"]},
        "user-location-region-user-device-os": {"group_by": ["user.location.region", "user.device.os"]},
        "user-location-region-user-device-network": {"group_by": ["user.location.region", "user.device.network"]},
        "user-location-metro-user-gender": {"group_by": ["user.location.metro", "user.gender"]},
        "user-location-metro-user-language": {"group_by": ["user.location.metro", "user.language"]},
        "user-location-metro-user-interest": {"group_by": ["user.location.metro", "user.interest"]},
        "user-location-metro-user-tv-genre": {"group_by": ["user.location.metro", "user.tv.genre"]},
        "user-location-metro-user-location-country": {"group_by": ["user.location.metro", "user.location.country"]},
        "user-location-metro-user-location-region": {"group_by": ["user.location.metro", "user.location.region"]},
        "user-location-metro-user-device-os": {"group_by": ["user.location.metro", "user.device.os"]},
        "user-location-metro-user-device-network": {"group_by": ["user.location.metro", "user.device.network"]},
        "user-device-os-user-gender": {"group_by": ["user.device.os", "user.gender"]},
        "user-device-os-user-language": {"group_by": ["user.device.os", "user.language"]},
        "user-device-os-user-interest": {"group_by": ["user.device.os", "user.interest"]},
        "user-device-os-user-tv-genre": {"group_by": ["user.device.os", "user.tv.genre"]},
        "user-device-os-user-location-country": {"group_by": ["user.device.os", "user.location.country"]},
        "user-device-os-user-location-region": {"group_by": ["user.device.os", "user.location.region"]},
        "user-device-os-user-location-metro": {"group_by": ["user.device.os", "user.location.metro"]},
        "user-device-os-user-device-network": {"group_by": ["user.device.os", "user.device.network"]},
        "user-device-network-user-gender": {"group_by": ["user.device.network", "user.gender"]},
        "user-device-network-user-language": {"group_by": ["user.device.network", "user.language"]},
        "user-device-network-user-interest": {"group_by": ["user.device.network", "user.interest"]},
        "user-device-network-user-tv-genre": {"group_by": ["user.device.network", "user.tv.genre"]},
        "user-device-network-user-location-country": {"group_by": ["user.device.network", "user.location.country"]},
        "user-device-network-user-location-region": {"group_by": ["user.device.network", "user.location.region"]},
        "user-device-network-user-location-metro": {"group_by": ["user.device.network", "user.location.metro"]},
        "user-device-network-user-device-os": {"group_by": ["user.device.network", "user.device.os"]}
    }
    return groupings


def set_access_token():
    ConfigFile.set_property("gnip.cfg", "oauth", "token", sys.argv[2])
    return


def set_access_token_secret():
    ConfigFile.set_property("gnip.cfg", "oauth", "tokensecret", sys.argv[2])
    return


def set_consumer_key():
    ConfigFile.set_property("gnip.cfg", "oauth", "consumerkey", sys.argv[2])
    return


def set_consumer_secret():
    ConfigFile.set_property("gnip.cfg", "oauth", "consumersecret", sys.argv[2])
    return


def create_followed_segment():
    segment_name = sys.argv[2]
    user_id = sys.argv[3:]
    audience = get_audience_object()
    response = audience.create_segment_from_followers(segment_name, user_id)
    print (response.text)
    return


def create_engagement_segment():
    segment_name = sys.argv[2]
    user_id = sys.argv[3:]
    audience = get_audience_object()
    response = audience.create_segment_from_engaged(segment_name, user_id)
    print(response.text)
    return


def create_impressed_segment():
    segment_name = sys.argv[2]
    user_id = sys.argv[3:]
    audience = get_audience_object()
    response = audience.create_segment_from_impressed(segment_name, user_id)
    print(response.text)
    return


def create_tailored_segment():
    segment_name = sys.argv[2]
    audience_ids = sys.argv[3:]
    audience = get_audience_object()
    response = audience.create_segment_from_tailored(segment_name, audience_ids)
    print(response.text)


def create_segment():
    audience = get_audience_object()
    segment_create_response = audience.create_segment(sys.argv[2])
    if segment_create_response.status_code == requests.codes.created:
        print(json.dumps(segment_create_response.json()))
    else:
        if segment_create_response.status_code == requests.codes.unauthorized:
            print('{"errors":["Create Segment Error - Unauthorized.  Check keys and tokens"]}')
        else:
            print(segment_create_response.text)
    return


def append_segment():
    audience = get_audience_object()
    segment_upload_size = 100000
    segment_name = sys.argv[2]
    user_id_filename = sys.argv[3]

    id_list = []
    append_to_id = None

    segments = audience.get_segments()
    if segments.status_code == requests.codes.ok:
        for segment in segments.json()['segments']:
            if segment['name'] == segment_name:
                append_to_id = segment['id']
        print("  Segment id:", append_to_id)
    elif segments.status_code == requests.codes.unauthorized:
        print('{"errors":["Segment Append Error - Unauthorized.  Check keys and tokens"]}')
    else:
        print(segments.text)

    if append_to_id is not None:
        try:
            with open(user_id_filename) as user_id_file:
                for user_id in user_id_file:
                    if 5 < len(user_id) < 20:
                        id_list.append(user_id[:-1])
        except IOError:
            print('{"errors":["Cannot Find or open: ' + user_id_filename + '"]}')

        loop_flag = True
        start_id = 0

        while loop_flag:
            if len(id_list) < segment_upload_size:
                max_id = len(id_list)
            else:
                max_id = segment_upload_size

            segment_append_response = audience.append_to_segment(append_to_id, id_list[start_id:max_id])
            if segment_append_response.status_code == requests.codes.ok:
                print(json.dumps(segment_append_response.json()))
                del id_list[start_id:max_id]
                if max_id < segment_upload_size:
                    loop_flag = False
            elif segment_append_response.status_code == requests.codes.unauthorized:
                print('{"errors":["Append Segment Error - Unauthorized.  Check keys and tokens"]}')
                loop_flag = False
            else:
                print(segment_append_response.text)
    return


def create_audience():
    audience_name = sys.argv[2]
    segment_name = []

    audience = get_audience_object()

    for arg in sys.argv[3:]:
        segment_name.append(arg)

    segment_ids = []
    segments = audience.get_segments()

    if segments.status_code == requests.codes.ok:
        for SEGMENT_NAME in segment_name:
            for segment in segments.json()['segments']:
                if segment['name'] == SEGMENT_NAME:
                    segment_ids.append(segment['id'])
    else:
        if segments.status_code == requests.codes.unauthorized:
            print('{"errors":["Create Audience Error (get_segments) - Unauthorized.  Check keys and tokens"]}')
        else:
            print(segments.text)

    if len(segment_ids) > 0:
        audience_create_response = audience.create_audience(audience_name, segment_ids)
        if audience_create_response.status_code == requests.codes.created:
            print(json.dumps(audience_create_response.json()))
        elif audience_create_response.status_code == requests.codes.unauthorized:
            print('{"errors":["Audience Create Error - Unauthorized.  Check keys and tokens"]}')
        else:
            print(audience_create_response.text)
    else:
        print('{"errors":["Create Audience Error - No valid segments Found."]}')
    return


def query_audience():
    audience_name = sys.argv[2]
    groupings = get_groupings()
    query_groupings = {}
    errors = []
    error_flag = False
    for arg in sys.argv[3:]:
        if arg in groupings:
            query_groupings[arg] = groupings[arg]
        else:
            errors.append({"Grouping: " + arg + " not found."})
            error_flag = True

    if error_flag:
        error_message = {"errors": errors}
        print(error_message)

    else:
        audience = get_audience_object()
        get_audiences_response = audience.get_audiences()
        if get_audiences_response.status_code == requests.codes.ok:
            for audience_item in get_audiences_response.json()['audiences']:
                if audience_item["name"] == audience_name:
                    query = {"groupings": query_groupings}
                    audience_query_response = audience.get_audience_query(audience_item["id"], query)
                    if audience_query_response.status_code == requests.codes.ok:
                        print(json.dumps(audience_query_response.json()))
                    elif audience_query_response.status_code == requests.codes.unauthorized:
                        print('{"errors":["Audience Query Error - Unauthorized.  Check keys and tokens"]}')
                    else:
                        print(audience_query_response.text)
        else:
            if get_audiences_response.status_code == requests.codes.unauthorized:
                print('{"errors":["Query Audience Error (get-audiences) - Unauthorized.  Check keys and tokens"]}')
            else:
                print(get_audiences_response.text)
    return


def delete_audience():
    audience_name = sys.argv[2]
    audience = get_audience_object()
    get_audiences_response = audience.get_audiences()
    if get_audiences_response.status_code == requests.codes.ok:
        for audience_item in get_audiences_response.json()['audiences']:
            if audience_item["name"] == audience_name:
                audience_delete_response = audience.delete_audience(audience_item['id'])
                if audience_delete_response.status_code == requests.codes.ok:
                    print(json.dumps(audience_delete_response.json()))
                else:
                    print(audience_delete_response.text)
    elif get_audiences_response.status_code == requests.codes.unauthorized:
        print('{"errors":["Delete Audience Error (get audiences)- Unauthorized.  Check keys and tokens"]}')

    else:
        print(get_audiences_response.text)
    return


def delete_segment():
    segment_name = sys.argv[2]
    audience = get_audience_object()
    segments = audience.get_segments()
    if segments.status_code == requests.codes.ok:
        deleted_success = False
        for segment in segments.json()['segments']:
            if segment["name"] == segment_name:
                audience = get_audience_object()
                segment_delete_response = audience.delete_segment(segment['id'])
                if segment_delete_response.status_code == requests.codes.ok:
                    deleted_success = True
                    segment["state"] = "deleted"
                    segment["last_modified"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    # print (str(segment))
                    print(json.dumps(segment))
                else:
                    if segment_delete_response.status_code == requests.codes.unauthorized:
                        print('{"errors":["Delete Segment Error - Unauthorized.  Check keys and tokens"]}')
                    else:
                        print(segment_delete_response.text)
        if not deleted_success:
            print('{"error":"Segment ' + segment_name + ' not found. unable to delete"}')
    elif segments.status_code == requests.codes.unauthorized:
        print('{"errors":["Delete Segment Error(get_segments) - Unauthorized.  Check keys and tokens"]}')
    else:
        print(segments.text)
    return


def list_audiences():
    audience = get_audience_object()
    audiences_response = audience.get_audiences()
    if audiences_response.status_code == requests.codes.ok:
        print(json.dumps(audiences_response.json()))
    elif audiences_response.status_code == requests.codes.unauthorized:
        print('{"errors":["List Audiences Error - Unauthorized.  Check keys and tokens"]}')
    else:
        print(audiences_response.text)
    return


def list_segments():
    audience = get_audience_object()
    segments_response = audience.get_segments()
    if segments_response.status_code == requests.codes.ok:
        print(json.dumps(segments_response.json()))
    elif segments_response.status_code == requests.codes.unauthorized:
        print('{"errors":["List Segments Error - Unauthorized.  Check keys and tokens"]}')
    else:
        print(segments_response.text)
    return


def list_grouping_names():
    groupings = get_groupings()
    print('{"groupings":["', end="")
    print('","'.join(map(str, sorted(groupings.keys()))), end="")
    print('"]}')
    return


def get_usage():
    audience = get_audience_object()
    usage_response = audience.get_usage()
    if usage_response.status_code == requests.codes.ok:
        print(json.dumps(usage_response.json()))
    elif usage_response.status_code == requests.codes.unauthorized:
        print('{"errors":["Usage - Unauthorized.  Check keys and tokens"]}')
    else:
        print(usage_response.text)
    return


if __name__ == "__main__":
    arg_count_check(1)
    action = sys.argv[1]

    if action.lower() == "set-access-token":
        arg_count_check(1)
        set_access_token()
    elif action.lower() == "set-access-token-secret":
        arg_count_check(1)
        set_access_token_secret()
    elif action.lower() == "set-consumer-key":
        arg_count_check(1)
        set_consumer_key()
    elif action.lower() == "set-consumer-secret":
        arg_count_check(1)
        set_consumer_secret()
    elif action.lower() == "create-segment":
        arg_count_check(2)
        create_segment()
    elif action.lower() == "create-followed-segment":
        arg_count_check(2)
        create_followed_segment()
    elif action.lower() == "create-engagement-segment":
        arg_count_check(2)
        create_engagement_segment()
    elif action.lower() == "create-impressed-segment":
        arg_count_check(2)
        create_impressed_segment()
    elif action.lower() == "create-tailored-segment":
        arg_count_check(2)
        create_tailored_segment()
    elif action.lower() == "append-segment":
        arg_count_check(3)
        append_segment()
    elif action.lower() == "create-audience":
        arg_count_check(3)
        create_audience()
    elif action.lower() == "query-audience":
        arg_count_check(3)
        query_audience()
    elif action.lower() == "delete-audience":
        arg_count_check(2)
        delete_audience()
    elif action.lower() == "delete-segment":
        arg_count_check(2)
        delete_segment()
    elif action.lower() == "list-audiences":
        list_audiences()
    elif action.lower() == "list-segments":
        list_segments()
    elif action.lower() == "list-groupings":
        list_grouping_names()
    elif action.lower() == "usage":
        get_usage()
    else:
        parameter_help()
