#!/usr/bin/env python3
from googleapiclient.discovery import build
import json
import csv

#PAGETOKEN='CLwFEAA' # set to none to start the search anew from scratch
#counter = 12
PAGETOKEN = ''
counter = 0

with open('../apikeys/google_api_key_youtube_tyler.txt','r') as keyfile:
    api_key = keyfile.read().strip()

youtube_service = build('youtube', 'v3', developerKey=api_key)

search_request = youtube_service.search().list(part='snippet', q='forsage', type='video', publishedAfter='2020-01-01T00:00:00Z', safeSearch='none', maxResults='50', order='viewCount', pageToken=PAGETOKEN)

with open('../data/youtube_forsage_search.csv','a') as csv_file:
    csv_writer = csv.writer(csv_file)

    while search_request:
        search_response = search_request.execute()
        print('Response #{} {}'.format(counter, PAGETOKEN))
        #print(json.dumps(response, sort_keys=True, indent=4))
        for element in search_response['items']:
            #print(element['snippet']['title'])
            print(element['snippet']['title'])

            video_title = element['snippet']['title']
            video_id = element['id']['videoId']
            video_published_at = element['snippet']['publishedAt']
            video_description = element['snippet'].get('description','')

            channel_title = element['snippet']['channelTitle']
            channel_id = element['snippet']['channelId']

            video_request = youtube_service.videos().list(part='statistics', id=video_id)
            video_response = video_request.execute()

            if len(video_response['items']) == 0:
                video_view_count = ''
            else:
                video_view_count = video_response['items'][0]['statistics']['viewCount']

            channel_request = youtube_service.channels().list(part='snippet,statistics', id=(element['snippet']['channelId']))
            channel_response = channel_request.execute()

            if len(video_response['items']) == 0:
                channel_country = ''
                channel_subscriber_count = ''
                channel_published_at = ''
                channel_sum_video_count = ''
                channel_sum_view_count = ''
                channel_description = ''
            else:
                channel_country = channel_response['items'][0]['snippet'].get('country', '')
                channel_subscriber_count = channel_response['items'][0]['statistics']['subscriberCount']
                channel_published_at = channel_response['items'][0]['snippet']['publishedAt']
                channel_sum_video_count = channel_response['items'][0]['statistics']['videoCount']
                channel_sum_view_count = channel_response['items'][0]['statistics']['viewCount']
                channel_description = channel_response['items'][0]['snippet'].get('description','')

            out_row = [
                    video_title, video_id, video_view_count, video_published_at, video_description,
                    channel_title, channel_id, channel_sum_view_count, channel_published_at,
                    channel_sum_video_count, channel_subscriber_count, channel_country, channel_description
            ]
            csv_writer.writerow(out_row)
        PAGETOKEN = search_response.get("nextPageToken")
        search_request = youtube_service.search().list_next(search_request, search_response)
        counter += 1

