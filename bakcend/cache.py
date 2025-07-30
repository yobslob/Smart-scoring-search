import redis
import json
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

def get_parsed_query(keyword):
    cache_key = f"parsed_query:{keyword}"
    cached = r.get(cache_key)
    if cached:
        print(f"DEBUG: Cache hit for keyword: '{keyword}'")
        return json.loads(cached)
    else:
        print(f"DEBUG: Cache miss for keyword: '{keyword}'. Calling query_parser.parse_query.")
        from query_parser import parse_query
        parsed = parse_query(keyword)
        print(f"DEBUG: Caching result for '{keyword}': {parsed}")
        r.set(cache_key, json.dumps(parsed), ex=3600)  # Cache for 1 hour
        return parsed