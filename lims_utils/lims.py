import json
import os
from urllib.parse import urljoin

import requests

base_url = "https://lims.minneapolismn.gov/"


class LimsApi:
    def __init__(self):
        self.session = requests.Session()
        self.key = os.getenv("LIMS_KEY")
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.key}",
            }
        )

    def searchMeetingCalendar(self, params):
        """
        params = {
            "CalendarYear": 2021, # Required
            "MeetingBodyAbbreviation": null,
            "MeetingDateFrom": null,
            "MeetingDateTo": null,
            "MemberId": null
        }
        """
        url = urljoin(base_url, "/api/v1/search/meetingCalendar")
        resp = self.session.post(url=url, json=params)
        resp.raise_for_status()
        return resp

    def getMeetingBodies(self):
        """
        returns   {
            "Abbreviation": "PHS",
            "Name": "Public Health & Safety Committee",
            "Type": "Council",
            "IsCurrent": True
        }
        """
        url = urljoin(base_url, "/api/v1/referenceList/MeetingBodies")
        resp = self.session.get(url=url)
        resp.raise_for_status()
        return resp
