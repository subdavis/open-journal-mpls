from dateutil.parser import parse as date_parse
from dotenv import load_dotenv
from time import sleep

from lims_utils.claude import generate_summary
from lims_utils.meetings import update_meeting_cache, load_meeting_cache
from lims_utils.transcript import formatSummaryForHugo
load_dotenv()


def updateCache():
    update_meeting_cache("2024-01-01")


def generate():
    cacheList = load_meeting_cache()
    # Get cached meetings sorted by date
    cachedMeetings = sorted(
        cacheList, key=lambda x: date_parse(x["meetingTime"]), reverse=True
    )

    for meeting in (cachedMeetings[:8]):
        filename, text, isNewContent = generate_summary(meeting)
        if text and filename:
            formatSummaryForHugo(meeting, text)
            if isNewContent:
                print(f"Summary for {meeting['committeeName']}::{meeting['meetingTime']} written to {filename}. Sleeping...")
                sleep(120)