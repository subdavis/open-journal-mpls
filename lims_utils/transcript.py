import random
from time import sleep

from pathlib import Path
from dateutil.parser import parse as date_parse
from youtube_transcript_api import (NoTranscriptAvailable, NoTranscriptFound,
                                    YouTubeTranscriptApi)

from lims_utils.utils import archivePath, load_file, save_file, save_text


# This function takes a transcript as a list of objects
# Described: [{text: 'string', start: float, duration: float}]
# Lines will begin with >> to indicate a new speaker
# This function returns a text file.
# Each line will be 100 characters long max
# New speakers will always begin on a new line
# The line will begin with the start time of the earliest entry on that line
def format_transcript(transcript: list) -> str:
    document = ""
    lineBuffer = ""
    # lineStart = 0
    for entry in transcript:
        text = entry["text"].strip()
        entryStart = str(entry["start"])
        # If the line has outgrown the limit, flush the buffer
        if (len(lineBuffer)) > 80:
            document += f"{lineBuffer}\n"
            lineBuffer = ""
            # lineStart = "{:.2f}".format(entryStart)
        # If the text is a new speaker, flush the buffer
        if text.startswith(">>"):
            if lineBuffer:
                document += f"{lineBuffer}\n"
            lineBuffer = text
            # lineStart = "{:.2f}".format(entryStart)
        elif lineBuffer:
            lineBuffer += " " + text
        else:
            lineBuffer += "   " + text
    if lineBuffer:
        document += f"{lineBuffer}\n"
    return document


def getTranscriptForMeeting(meeting):
    if meeting["mainVideoURL"]:
        video_id = meeting["mainVideoURL"]
        if "youtube.com" in video_id:
            video_id = video_id.split("v=")[-1].split("&")[0]
        elif "youtu.be" in video_id:
            video_id = video_id.split("/")[-1].split("?")[0]
        transcript_filename = archivePath / "transcript" / f"transcript_{video_id}.json"
        transcript = load_file(transcript_filename)
        if transcript is not None:
            print(f"Cache: Transcript for {video_id} already exists")
        else:
            print(f"Getting transcript for {video_id}")
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                save_file(transcript_filename, transcript)
                sleep(random.uniform(8, 12))
            except (NoTranscriptFound, NoTranscriptAvailable):
                print(f"No transcript available for {video_id}")
                save_file(transcript_filename, [])
                sleep(random.uniform(8, 12))
        return transcript, video_id
    return None, None

def formatSummaryForHugo(meeting, summary_text):
    meetingTime = date_parse(meeting["meetingTime"])
    committeeName = meeting["committeeName"]
    fileTitle = committeeName.replace(" ", "-").replace('&', 'and').replace(",", "").lower()
    filename = Path("blog") / "content" / "posts" / f"{fileTitle}-{meetingTime.date()}.md"
    
    documentHeader = "+++" \
                    f"\ntitle = \"{committeeName}\"" \
                    f"\ndate = {meetingTime.date()}" \
                    "\n generated = true" \
                    f"\n[params]" \
                    f"\n  author = \"Claude.ai\"" \
                    "\n+++\n\n"
    save_text(filename, documentHeader + summary_text)
