import logging
import re
from re import Match
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def is_valid_name(name: str) -> bool:
    match: Match = re.match('^[A-Za-zА-Яа-я\' ]+$', name)
    return len(name) > 0 and match != None and len(name) <= 100

def is_valid_group(name: str) -> bool:
    return len(name) > 0 and len(name) <= 100
