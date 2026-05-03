import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_PATH = os.path.join(BASE_DIR, 'database', 'sample_data.json')

try:
    with open(DATA_PATH, 'r', encoding='utf-8') as _f:
        SAMPLE_DATA = json.load(_f)
except FileNotFoundError:
    SAMPLE_DATA = {}


def get_sample_data():
    return SAMPLE_DATA


def get_section(section_name, default=None):
    return SAMPLE_DATA.get(section_name, default if default is not None else {})


def get_cases():
    return SAMPLE_DATA.get('cases', [])


def get_auth():
    return SAMPLE_DATA.get('auth', {})


def get_report():
    return SAMPLE_DATA.get('report', {})
