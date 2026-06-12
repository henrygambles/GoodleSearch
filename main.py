import os
import re
import sys
import asyncio
import aiohttp
import requests

# Ensure token is set
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
if not GENIUS_ACCESS_TOKEN:
    print("❌ Error: GENIUS_ACCESS_TOKEN environment variable not set.")
    sys.exit(1)

# Mimic a web browser to prevent Cloudflare blocks
HEADERS = {
    "Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
# Expanded to capture 1960s soul, gospel, and torch-song vernacular
KEYWORDS_PATTERN = re.compile(r'\b(god|lord|prayer|pray|heaven|angel|angels)\b', re.IGNORECASE)
# Global control event for the async animation loop
animation_event = asyncio.Event()

def clear_terminal():
    """Cleans the screen reliably based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

async def god_animation():
    """Asynchronous loop animating the celestial entity while workers fetch data."""
    frame_a = """
             .---.
          .-(     )-.
         (___________)
          /         \\
         |  _     _  |
         | (o)   (o) |   <- [ THE OMNIPRESENT ]
         |     V     |
          \\   ---   /
           '-------'
             /   \\
            /|   |\\
           / |   | \\
          v  |   |  v
            /     \\
           /       \\
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ⚡ Gathering cosmic frequencies...
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """

    frame_b = """
         ✨  .---.  ✨
          .-(     )-.
         (___________)
          /         \\
         |  _     _  |
         | (•)   (•) |   <- [ THE OMNIPRESENT ]
         |     #     |
          \\   ===   /
           '-------'
            // | | \\\\
           //  | |  \\\\
          //   | |   \\\\
          v    | |    v
              /   \\
             /     \\
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ✨ Hyper-scanning Genius Database...
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    
    frames = [frame_a, frame_b]
    i = 0
    
    # Run loop until main task sets the completion event
    while not animation_event.is_set():
        clear_terminal()
        sys.stdout.write(frames[i % 2])
        sys.stdout.flush()
        i += 1
        await asyncio.sleep(0.4)
        
    clear_terminal()

def safe_get_json(url, params=None):
    """Safely executes a standard GET request for indexing."""
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if response.status_code != 200:
            return None
        return response.json()
    except Exception:
        return None

def fetch_all_track_urls(artist_name):
    """Rapidly queries metadata indexing endpoints."""
    search_url = "https://api.genius.com/search"
    response = safe_get_json(search_url, params={"q": artist_name})
    if not response:
        return None, []
        
    hits = response.get("response", {}).get("hits", [])
    if not hits:
        return None, []
        
    primary_artist_id = hits[0]["result"]["primary_artist"]["id"]
    actual_artist_name = hits[0]["result"]["primary_artist"]["name"]
    
    songs = []
    page = 1
    
    while page:
        artists_songs_url = f"https://api.genius.com/artists/{primary_artist_id}/songs"
        res = safe_get_json(artists_songs_url, params={"page": page, "per_page": 50})
        if not res:
            break
            
        page_songs = res.get("response", {}).get("songs", [])
        if not page_songs:
            break
            
        songs.extend(page_songs)
        page = res.get("response", {}).get("next_page")
        
    return actual_artist_name, [(s["title"], s["url"]) for s in songs if s["lyrics_state"] == "complete"]

async def scrape_and_scan_lyrics(session, semaphore, title, url):
    """Worker task that processes a single lyric layout sheet."""
    async with semaphore:
        try:
            async with session.get(url, headers={"User-Agent": HEADERS["User-Agent"]}, timeout=10) as response:
                if response.status != 200:
                    return None
                html = await response.text()
                
                lyric_divs = re.findall(r'data-lyrics-container="true"[^>]*>(.*?)</div>', html, re.DOTALL)
                if not lyric_divs:
                    return None
                    
                clean_lyrics = re.sub(r'<[^>]+>', '\n', "".join(lyric_divs))
                
                song_references = []
                for line_num, line in enumerate(clean_lyrics.split('\n'), 1):
                    matches = KEYWORDS_PATTERN.findall(line)
                    if matches:
                        song_references.append({
                            "line": line_num,
                            "text": line.strip(),
                            "matches": list(set([m.lower() for m in matches]))
                        })
                        
                return {"title": title, "references": song_references} if song_references else None
        except Exception:
            return None

async def main():
    user_input = input("Enter artist name [Default: Bob Dylan]: ").strip()
    artist_name = user_input if user_input else "Bob Dylan"
    
    print("✨ Preparing connection array...")
    
    # 1. Fetch metadata indexing maps
    actual_name, track_list = fetch_all_track_urls(artist_name)
    if not track_list:
        print("❌ No track URLs could be retrieved.")
        return
        
    # 2. Fire up the background animation task
    animation_event.clear()
    anim_task = asyncio.create_task(god_animation())
    
    # 3. Fire up concurrent workers to hyper-scan text pages
    sem = asyncio.Semaphore(10) 
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_and_scan_lyrics(session, sem, title, url) for title, url in track_list]
        results = await asyncio.gather(*tasks)
        
    # 4. Kill the animation cleanly when operations end
    animation_event.set()
    await anim_task

    valid_results = [r for r in results if r]
    
    print(f"=== HIGH-SPEED REPORT FOR {actual_name.upper()} ===")
    print(f"Scanned {len(track_list)} tracks total.")
    if not valid_results:
        print("No matches detected.")
        return

    for song in valid_results:
        print(f"\n🎵 Song: {song['title']}")
        print("-" * 40)
        for ref in song['references']:
            print(f"  [Line {ref['line']} | Found: {', '.join(ref['matches'])}]: \"{ref['text']}\"")

if __name__ == "__main__":
    asyncio.run(main())