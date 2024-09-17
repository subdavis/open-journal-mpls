import os

import anthropic

from lims_utils.prompts import city_council_meeting_prompt
from lims_utils.transcript import format_transcript, getTranscriptForMeeting
from lims_utils.utils import archivePath, load_text, save_text


def generate_summary(meeting):
    client = anthropic.Anthropic()
    client.api_key = os.getenv("ANTHROPIC_KEY")
    committeeName = meeting["MeetingBody"]
    meetingTime = meeting["MeetingDateTime"]
    transcript_to_analyze, videoId = getTranscriptForMeeting(meeting)

    if transcript_to_analyze is None:
        return None, None, False

    summary_filename = archivePath / "summary" / f"summary_{videoId}.md"
    document = load_text(summary_filename)

    if document is not None:
        print(f"Cache: Summary for {videoId} already exists")
        return summary_filename, document, False

    transcript_text = format_transcript(transcript_to_analyze)
    full_prompt = city_council_meeting_prompt.format(transcript_text=transcript_text)
    token_estimate = client.count_tokens(full_prompt)
    print(
        f"Generate summary with inputTokens={token_estimate} for {committeeName}::{meetingTime}::{videoId}"
    )
    message = client.messages.create(
        max_tokens=5000,
        messages=[
            {
                "role": "user",
                "content": full_prompt,
            }
        ],
        model="claude-3-5-sonnet-20240620",
    )

    document = ""
    for line in message.content:
        document += line.text + "\n"
    save_text(summary_filename, document)
    return summary_filename, document, True
