"""Configure the search engine."""
import pathlib

SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]

SEARCH_ROOT = pathlib.Path(__file__).resolve().parent.parent

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = SEARCH_ROOT/'search'/'var'/'index.sqlite3'
