import requests
from yt_dlp import YoutubeDL
import re

def get_clean_transcript(video_id):
    """Gets and formats YouTube transcript with better error handling"""
    try:
        # Configure yt-dlp to avoid format download errors
        ydl_opts = {
            'quiet': True,
            'skip_download': True,  # Skip downloading video formats
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://youtube.com/watch?v={video_id}", download=False)
        
        print("✅ Video title:", info.get("title", "Unknown"))
        
        # Try to get transcript data
        transcript_text = None
        
        # Method 1: Check for automatic captions
        if not transcript_text:
            auto_captions = info.get('automatic_captions', {})
            if 'en' in auto_captions:
                transcript_url = None
                for fmt in auto_captions['en']:
                    if fmt.get('ext') in ['json3', 'vtt', 'srv3', 'srv1', 'ttml']:
                        transcript_url = fmt['url']
                        break
                
                if transcript_url:
                    transcript_text = download_and_parse_transcript(transcript_url, 'auto')
        
        # Method 2: Check for manual subtitles
        if not transcript_text:
            subtitles = info.get('subtitles', {})
            if 'en' in subtitles:
                transcript_url = None
                for fmt in subtitles['en']:
                    if fmt.get('ext') in ['json3', 'vtt', 'srv3', 'srv1', 'ttml']:
                        transcript_url = fmt['url']
                        break
                
                if transcript_url:
                    transcript_text = download_and_parse_transcript(transcript_url, 'manual')
        
        if transcript_text:
            # Clean and limit transcript length
            cleaned = ' '.join(transcript_text.split()[:400])  # Limit to ~400 words
            if len(transcript_text.split()) > 400:
                cleaned += '...'
            return cleaned
        else:
            return "Error: No English transcript available for this video"
    
    except Exception as e:
        return f"Error getting transcript: {str(e)}"

def download_and_parse_transcript(url, caption_type):
    """Download and parse transcript from URL"""
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        content = response.text
        print(f"📥 Downloaded {caption_type} captions")
        
        # Parse based on format (simplified parsing)
        if url.endswith('.json3') or 'json3' in url:
            return parse_json3_transcript(response.json())
        elif url.endswith('.vtt') or 'vtt' in url:
            return parse_vtt_transcript(content)
        else:
            # Generic text cleanup for other formats
            return clean_transcript_text(content)
            
    except Exception as e:
        print(f"Error parsing {caption_type} transcript: {e}")
        return None

def parse_json3_transcript(json_data):
    """Parse YouTube's JSON3 transcript format"""
    lines = []
    try:
        for event in json_data.get('events', []):
            if 'segs' in event:
                for seg in event['segs']:
                    text = seg.get('utf8', '').strip()
                    if text and not text.startswith('['):
                        lines.append(text)
        return ' '.join(lines)
    except:
        return None

def parse_vtt_transcript(vtt_content):
    """Parse WebVTT format"""
    lines = []
    for line in vtt_content.splitlines():
        clean_line = line.strip()
        if (clean_line and 
            not clean_line.startswith(('WEBVTT', 'NOTE', 'STYLE', '-->')) and
            not re.match(r'^\d{2}:\d{2}', clean_line)):
            lines.append(clean_line)
    return ' '.join(lines)

def clean_transcript_text(text):
    """Generic transcript text cleaning"""
    # Remove XML/HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove timestamps and other metadata
    text = re.sub(r'\d{1,2}:\d{2}:\d{2}\.\d{3}', '', text)
    text = re.sub(r'\d{1,2}:\d{2}\.\d{3}', '', text)
    # Clean up extra whitespace
    text = ' '.join(text.split())
    return text

# Alternative approach using YouTube Transcript API
def get_transcript_alternative(video_id):
    """Alternative method using youtube-transcript-api if available"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([item['text'] for item in transcript_list])
        return transcript_text[:2000] + ('...' if len(transcript_text) > 2000 else '')
    except ImportError:
        return "youtube-transcript-api not installed"
    except Exception as e:
        return f"Alternative method failed: {str(e)}"

# 🔽 TEST with different videos
test_videos = [
    "xbxQxK6gFnI",  # Rick Astley - Never Gonna Give You Up
    "dQw4w9WgXcQ",  # Another Rickroll version
    "jNQXAC9IVRw",  # First YouTube video (might have captions)
]

print("Testing transcript extraction...")
for video_id in test_videos:
    print(f"\n🎬 Testing video: {video_id}")
    transcript = get_clean_transcript(video_id)
    print(f"Transcript preview: {transcript[:200]}...")
    
    # Try alternative method if main one fails
    if "Error" in transcript:
        print("Trying alternative method...")
        alt_transcript = get_transcript_alternative(video_id)
        print(f"Alternative result: {alt_transcript[:200]}...")


