"""
Extracts all video titles and URLs from a YouTube playlist using the official YouTube Data API.
Generates a playlist_titles.csv file with: position, title, channel, url.

Requirements:
    pip install google-api-python-client

Usage:
    python extract_playlist.py
    (it will ask you for your API key and the playlist ID or URL)
"""

import csv
import re
from googleapiclient.discovery import build


def extract_playlist_id(text):
    """Accepts either a playlist ID or a full URL and returns the ID."""
    match = re.search(r"[?&]list=([a-zA-Z0-9_-]+)", text)
    if match:
        return match.group(1)
    # If it's not a URL, assume it's already the ID
    return text.strip()


def get_videos(youtube, playlist_id):
    videos = []
    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        ).execute()

        for item in response.get("items", []):
            snippet = item["snippet"]
            title = snippet.get("title", "")
            channel = snippet.get("videoOwnerChannelTitle", "")
            video_id = snippet.get("resourceId", {}).get("videoId", "")

            # Deleted/private videos show up with these generic titles
            if title in ("Deleted video", "Private video"):
                continue

            videos.append({
                "position": len(videos) + 1,
                "title": title,
                "channel": channel,
                "url": f"https://www.youtube.com/watch?v={video_id}" if video_id else "",
            })

        next_page_token = response.get("nextPageToken")
        print(f"  Downloaded: {len(videos)} videos...")

        if not next_page_token:
            break

    return videos


def main():
    print("=== YouTube Playlist Title Extractor ===\n")
    api_key = input("Paste your YouTube API key: ").strip()
    playlist_input = input("Paste the playlist URL or ID: ").strip()
    playlist_id = extract_playlist_id(playlist_input)

    youtube = build("youtube", "v3", developerKey=api_key)

    print(f"\nFetching videos from playlist {playlist_id}...")
    videos = get_videos(youtube, playlist_id)

    output_file = "playlist_titles.csv"
    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["Position", "Title", "Channel", "URL"])
        writer.writeheader()
        writer.writerows(videos)

    print(f"\nDone! Saved {len(videos)} videos to '{output_file}'")
    print("(Deleted or hidden videos were not included)")


if __name__ == "__main__":
    main()