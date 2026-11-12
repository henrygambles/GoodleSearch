# GoodleSearch

> *"Search for the divine — one lyric at a time."*

GoodleSearch is a command-line tool that scans an artist's entire Genius catalogue for spiritual and celestial references — words like **god**, **lord**, **angel**, **heaven**, **prayer**, and more. Powered by async concurrency and the Genius API, it tears through hundreds of songs in seconds and tells you exactly where the transcendence lives.

```
         ✨  .---.  ✨
          .-(     )-.
         (___________)
          /         \
         |  _     _  |
         | (•)   (•) |   <- [ THE OMNIPRESENT ]
         |     #     |
          \   ===   /
           '-------'
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ✨ Hyper-scanning Genius Database...
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

---

## Features

- **Full catalogue scans** — fetches every track with complete lyrics for any artist on Genius
- **Concurrent scraping** — up to 10 parallel workers tear through lyric pages at once
- **Precise line-level matches** — reports the exact line number, text, and matched keywords
- **Animated terminal UI** — a cosmic ASCII entity watches over the process so you don't get bored
- **Sensible default** — press Enter to scan Bob Dylan if you can't decide

---

## Requirements

- Python 3.8+
- A [Genius API](https://genius.com/api-clients) access token

Install dependencies:

```bash
pip install aiohttp requests
```

---

## Setup

1. Get a free API token at [genius.com/api-clients](https://genius.com/api-clients)
2. Export it into your environment:

```bash
export GENIUS_ACCESS_TOKEN="your_token_here"
```

---

## Usage

```bash
python main.py
```

You'll be prompted for an artist name. Hit Enter to use the default (Bob Dylan).

```
Enter artist name [Default: Bob Dylan]: Aretha Franklin
```

The omnipresent one will animate while the tool indexes the catalogue. When it finishes, you get a full report:

```
=== HIGH-SPEED REPORT FOR ARETHA FRANKLIN ===
Scanned 142 tracks total.

🎵 Song: Amazing Grace
----------------------------------------
  [Line 3 | Found: lord]: "O Lord, what a morning"
  [Line 7 | Found: angel]: "Angels keep watching over me"

🎵 Song: I Say a Little Prayer
----------------------------------------
  [Line 1 | Found: prayer, pray]: "I say a little prayer for you"
```

---

## Keywords Scanned

| Word | Word |
|------|------|
| god | lord |
| prayer | pray |
| heaven | angel |
| angels | |

The pattern is case-insensitive and matches whole words only, so `praying` won't trigger `pray` — keeping results clean.

---

## How It Works

1. **Search** — queries the Genius API to resolve the artist name and ID
2. **Index** — paginates through all songs with `lyrics_state: complete`
3. **Scrape** — asynchronously fetches raw HTML from each Genius lyrics page and strips tags
4. **Match** — runs the keyword regex line-by-line and collects hits with context
5. **Report** — prints every matched song and line to the terminal

---

## License

Do what thou wilt.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=henrygambles/GoodleSearch&type=Date)](https://star-history.com/#henrygambles/GoodleSearch&Date)
