import datetime
import html
import os
import re
from time import sleep

from dateutil import tz
from dateutil.parser import parse as date_parse
from pyyoutube import Client

CITY_PLAYLIST_ID = "UU1IHi7mIMbFhZo4j_H6QIsA"
CITY_CHANNEL_ID = "UC1IHi7mIMbFhZo4j_H6QIsA"
tzinfos = {"CDT": tz.gettz("US/Central")}


class YoutubeMatcher:
    def __init__(self):
        api_key = os.environ.get("YOUTUBE_API_KEY")
        self.client = Client(api_key=api_key)
        self.known_videos = []
        self.publishedBefore = datetime.datetime.now(datetime.timezone.utc)
        self.nextPageToken = None
        self.totalResults = 0

    def get_video_transcript(self, video_id):
        caption_resources = self.client.captions.list(part="snippet", video_id=video_id)
        caption_id = None
        for caption in caption_resources.items:
            if caption.snippet.language == "en":
                caption_id = caption.id
                break
        if caption_id is None:
            return None
        print(f"Downloading transcript for {video_id}: {caption_id}")
        return self.client.captions.download(caption_id)

    def get_uploads_from_channel(self, channel_id):
        response = self.client.playlistItems.list(
            part="snippet,contentDetails",
            playlist_id=channel_id,
            max_results=20,
            page_token=self.nextPageToken,
        )
        self.nextPageToken = response.nextPageToken
        self.totalResults = response.pageInfo.totalResults
        items = response.items
        self.known_videos += items
        self.publishedBefore = date_parse(
            items[-1].snippet.publishedAt, tzinfos=tzinfos
        )

    def find_video_for_meeting(self, meeting):
        meetingTime = date_parse(meeting["MeetingDateTime"] + " CDT", tzinfos=tzinfos)
        while self.publishedBefore > meetingTime:
            self.get_uploads_from_channel(CITY_PLAYLIST_ID)
            print(".", end="", flush=True)
            sleep(4)
        for item in self.known_videos:
            itemTitle = re.sub(" +", " ", html.unescape(item.snippet.title).lower())
            targetTitle = re.sub(" +", " ", meeting["VideoTitle"].lower())
            if itemTitle == targetTitle:
                return item
        return None
