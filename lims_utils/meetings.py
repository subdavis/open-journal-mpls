import random
from datetime import datetime
from time import sleep
from typing import Optional, Tuple

import cloudscraper
from dateutil.parser import parse as date_parse
from tenacity import retry, stop_after_attempt

from lims_utils.utils import archivePath, load_file, save_file

# Configuration
meeting_page_url = "https://lims.minneapolismn.gov/CityCouncil/Meetings"
all_meeting_bodies_json = "https://lims.minneapolismn.gov/CityCouncil/GetCommitteesBasedOnCommitteeType?committeeTypeList=1,3"
meetings_json = "https://lims.minneapolismn.gov/CityCouncil/CityCouncilMeetingsPagedList?abbreviation="
meetingCacheFile = "meeting_cache.json"


@retry(stop=stop_after_attempt(3))
def get_meeting_page(page: int) -> dict:
    scraper = cloudscraper.create_scraper()
    scraper.headers.update(
        {
            "Host": "lims.minneapolismn.gov",
            "Origin": "https://lims.minneapolismn.gov",
            "Referer": "https://lims.minneapolismn.gov/CityCouncil/Meetings",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
    )
    page_size = 10
    start = page * page_size
    formdata = f"draw=1&columns%5B0%5D%5Bdata%5D=CommitteeName&columns%5B0%5D%5Bname%5D=CommitteeName&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=MeetingDate&columns%5B1%5D%5Bname%5D=MeetingDate&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=MeetingDate&columns%5B2%5D%5Bname%5D=MeetingDate&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=Video&columns%5B3%5D%5Bname%5D=Video&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=DESC&start={start}&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false"
    meetings = scraper.post(meetings_json, data=formdata)
    return meetings.json()


def load_meeting_cache() -> list:
    return load_file(archivePath / meetingCacheFile) or []


def update_meeting_cache(beginDateStr: Optional[str]) -> Tuple[list, list]:
    beginDateStr = beginDateStr or "2024-01-01"
    foundBeginDate = False
    foundCachedMeeting = False
    page = 0
    cacheList = load_meeting_cache()
    newMeetings = []
    cachedMeetingIdSet = set([meeting["id"] for meeting in cacheList])
    beginDate = date_parse(beginDateStr)

    # Look for either the first meeting we already know about or the first meeting before the begin date
    while (foundBeginDate or foundCachedMeeting) is False:
        print(f"Getting page {page}...")
        pageData = get_meeting_page(page)
        for meeting in pageData["data"]:
            meetingTime = date_parse(meeting["meetingTime"])
            if meeting["id"] in cachedMeetingIdSet:
                foundCachedMeeting = True
            elif meetingTime >= beginDate and meetingTime < datetime.now():
                if meeting["mainVideoURL"]:
                    print(
                        f"Discovered new meeting: {meeting['committeeName']} - {meeting['meetingTime']}"
                    )
                    newMeetings.append(meeting)
                else:
                    print(
                        f"Skipping meeting without video: {meeting['committeeName']} - {meeting['meetingTime']}"
                    )
            else:
                print(
                    f"Skipping future meeting: {meeting['committeeName']} - {meeting['meetingTime']}"
                )
            if meetingTime <= beginDate:
                foundBeginDate = True
        page += 1
        sleep(random.uniform(1, 3))

    save_file(archivePath / meetingCacheFile, cacheList + newMeetings)
    return cacheList, newMeetings
