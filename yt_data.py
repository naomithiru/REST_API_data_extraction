import sqlite3
import requests
import re

con = sqlite3.connect('aba_preach.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT  EXISTS information
                (video_id text PRIMARY KEY,	video_title text, upload_date text,	view_count integer,	like_count integer,	dislike_count integer, comment_count integer)''')



#cur.execute('''''')


def collect_channel_data(API_KEY, CHANNEL_ID):
    data = []

    pageToken = ""
    url = "https://www.googleapis.com/youtube/v3/search?key="+API_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=10000"+pageToken

    response = requests.get(url).json()

    for video in response['items']:
        if video['id']['kind'] == "youtube#video":
            video_id = video['id']['videoId']
            video_title = video['snippet']['title']
            upload_date = video['snippet']['publishTime']
            upload_date = str(upload_date).split("T")[0]

            url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&part=statistics&key="+API_KEY
            response_video_stats = requests.get(url_video_stats).json()
            view_count = response_video_stats['items'][0]['statistics']['viewCount']
            like_count = response_video_stats['items'][0]['statistics']['likeCount']
            dislike_count = response_video_stats['items'][0]['statistics']['dislikeCount']
            comment_count = response_video_stats['items'][0]['statistics']['commentCount']

            data.append((video_id, video_title, upload_date, view_count, like_count, dislike_count, comment_count))
    return data


def get_channel_id(API_KEY, USER_NAME):
    url = f'https://www.googleapis.com/youtube/v3/channels?key={API_KEY}&forUsername={USER_NAME}&part=id'
    response_channel = requests.get(url).json()
    channel_id = response_channel['items'][0]['id']
    return channel_id


API_KEY = "AIzaSyAh-7MUWJ0v6wd1ueTsLyTeoO-ceHfJuvs"
USER_NAME = "iProjectAtlas"

CHANNEL_ID = get_channel_id(API_KEY, USER_NAME)
data = collect_channel_data(API_KEY, CHANNEL_ID)
#print(data[0])

cur.executemany("INSERT OR IGNORE INTO information VALUES (?, ?, ?, ?, ?, ?, ?)", data)
con.commit()