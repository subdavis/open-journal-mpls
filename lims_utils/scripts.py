from datetime import datetime, timedelta
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
    # We're only interested in City Council and not other bodies
    bodiesOfInterest = filter(
        lambda x: x["Type"] == "Council" and x["IsCurrent"] is True, bodies
    )
    currentYear = datetime.now().year
    cutoff = timedelta(weeks=8)
    update_meeting_cache(currentYear, bodiesOfInterest, cutoff)


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
