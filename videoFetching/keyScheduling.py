
from . import API_KEYS , current_key_index

# Follows round scheduling of mulitple API keys, next key for next request
def get_next_key():
    global current_key_index
    key = API_KEYS[current_key_index]
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    return key