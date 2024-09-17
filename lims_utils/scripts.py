from time import sleep

from dateutil.parser import parse as date_parse
from dotenv import load_dotenv

from lims_utils.claude import generate_summary
from lims_utils.lims import LimsApi
from lims_utils.meetings import load_meeting_cache, update_meeting_cache
from lims_utils.transcript import formatSummaryForHugo

load_dotenv()


def updateCache():
    bodies = LimsApi().getMeetingBodies().json()
    bodiesOfInterest = filter(
        lambda x: x["Type"] == "Council" and x["IsCurrent"] is True, bodies
    )
    update_meeting_cache(2024, bodiesOfInterest)


def generate():
    cacheList = load_meeting_cache()
    # Get cached meetings sorted by date
    cachedMeetings = sorted(
        cacheList, key=lambda x: date_parse(x["MeetingDateTime"]), reverse=True
    )

    for meeting in cachedMeetings[:16]:
        filename, text, isNewContent = generate_summary(meeting)
        if text and filename:
            formatSummaryForHugo(meeting, text)
            if isNewContent:
                print(
                    f"Summary for {meeting['VideoTitle']} written to {filename}. Sleeping..."
                )
                sleep(120)
