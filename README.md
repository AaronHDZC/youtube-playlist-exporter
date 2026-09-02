# YouTube Playlist Title Extractor

Extracts all video titles, channel names, and URLs from a YouTube playlist
(including playlists with 1000+ videos) using the official YouTube Data API v3.

## Features
- Handles pagination automatically (fetches all videos, 50 at a time)
- Skips deleted/private videos
- Exports to CSV (UTF-8 with BOM, so accented characters display correctly in Excel)

## Requirements
- Python 3.x
- `google-api-python-client`

Install with:
```bash
pip install google-api-python-client
```

## Setup
1. Get a free API key from the [Google Cloud Console](https://console.cloud.google.com/)
   (enable the **YouTube Data API v3**).
2. Run the script and enter your API key and playlist URL/ID when prompted.

## Usage
```bash
python extract_playlist.py
```

## Output
A `playlist_titles.csv` file with columns: `position`, `title`, `channel`, `url`.

### Example:

<img width="1135" height="885" alt="image" src="https://github.com/user-attachments/assets/55d42e80-e679-48f8-bce1-cf3454741ad5" />

## License
MIT
