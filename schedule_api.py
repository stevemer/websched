import json
import time
import requests

class ScheduleApiError(Exception):
    '''
    Raised if there is an error with the schedule API.
    '''
    pass

# The base API endpoint
base_url = 'http://umich-schedule-api.herokuapp.com'

# the amount of time to wait for the schedule API
timeout_duration = 25


def get_data(relative_path):
    '''
    Gets data from the schedule API at the specified path.
    Will raise a ScheduleApiError if unsuccessful.
    Assumes API will return JSON, returns as a dictionary.
    '''

    timeout_at = time.time() + timeout_duration

    while time.time() < timeout_at:
        r = requests.get(base_url + relative_path)
        if r.status_code == 200:
            return json.loads(r.text)
        if r.status_code == 400:
            break

    raise ScheduleApiError('error for url: {0} message: "{1}" code: {2}' \
        .format(relative_path, r.text, r.status_code))

def get_terms():
    '''
    Returns a list of valid terms.
    Each item in the list is a dictionary containing:
        ('TermCode', 'TermDescr', 'TermShortDescr')
    '''
    return get_data('/get_terms')
