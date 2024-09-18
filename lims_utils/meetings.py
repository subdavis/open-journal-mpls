import random
from datetime import datetime, timedelta
from time import sleep
from typing import Optional, Tuple

from dateutil.parser import parse as date_parse

from lims_utils.lims import LimsApi
from lims_utils.utils import archivePath, load_file, save_file
from lims_utils.youtube import YoutubeMatcher

meetingCacheFile = "meeting_cache.json"


def video_title(meeting: dict) -> str:
    meetingTime = date_parse(meeting["MeetingDateTime"])
    formattedTime = meetingTime.strftime(
        "{dt:%B} {dt.day}, {dt.year}".format(dt=meetingTime)
    )
    formattedBody = meeting["MeetingBody"]
    if formattedBody == "City Council":
        formattedBody = "Minneapolis City Council"
    return f"{formattedTime} {formattedBody}"


def load_meeting_cache() -> list:
    return load_file(archivePath / meetingCacheFile) or []


def update_meeting_cache(
    calendarYear: str,
    bodiesOfInterest: list,
    cutoff: Optional[timedelta] = None,
) -> Tuple[list, list]:
    cacheList = load_meeting_cache()
    newMeetings = []
    cachedMeetingIdSet = set([meeting["VideoTitle"] for meeting in cacheList])
    youtubeClient = YoutubeMatcher()

    for body in bodiesOfInterest:
        print(f"Searching for meetings for {body['Abbreviation']}")
        data = LimsApi().searchMeetingCalendar(
            {
                "CalendarYear": calendarYear,
                "MeetingBodyAbbreviation": body["Abbreviation"],
            }
        )
        if data.status_code == 204:
            continue
        iterable = data.json()
        meetings = sorted(
            iterable, key=lambda x: date_parse(x["MeetingDateTime"]), reverse=True
        )
        for meeting in meetings:
            meetingTime = date_parse(meeting["MeetingDateTime"])
            meeting["VideoTitle"] = video_title(meeting)
            print(f"  Searching for {meeting['VideoTitle']}", end="", flush=True)
            if cutoff and meetingTime < (datetime.now() - cutoff):
                print(" - Meeting is too old.")
                break
            elif meeting["VideoTitle"] in cachedMeetingIdSet:
                print(" - Cached!")
                pass
            elif meetingTime < datetime.now():
                video = youtubeClient.find_video_for_meeting(meeting)
                if video:
                    meeting["VideoId"] = video.snippet.resourceId.videoId
                    print(" - Discovered!")
                    newMeetings.append(meeting)
                else:
                    print(" - No video found.")
            else:
                print(" - Future meeting.")
        save_file(archivePath / meetingCacheFile, cacheList + newMeetings)
        sleep(random.uniform(6, 8))

    return cacheList, newMeetings
