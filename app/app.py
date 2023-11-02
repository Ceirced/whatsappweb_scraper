from flask import Flask, render_template
import os
from collections import OrderedDict
import datetime
import sys
import os
import argparse
# Get the absolute path of the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Append the parent directory to sys.path
sys.path.append(parent_dir)

from user import User
from check_sync import get_users_in_db

app = Flask(__name__)

contact_names = get_users_in_db()

data = {}

for contact_name in contact_names:
    user = User(contact_name)
    for timestamp, status in user.statuses.items():
        data[timestamp] = {
            'name': user.name,
            'timestamp': timestamp,
            'timestamp_human': datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'),
            'status': status,
            'picture_id': user.profile_pictures.get(timestamp, '')
        }
    for timestamp, picture in user.profile_pictures.items():
        if timestamp not in data:
            data[timestamp] = {
                'name': user.name,
                'timestamp': timestamp,         #needed to sort the data
                'timestamp_human': datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'),
                'status': '',
                'picture_id': picture
            }
sorted_data = sorted(data.items(), key=lambda x: x[1]['timestamp'], reverse=True)

@app.route('/')
def index():
    return render_template('feed.html', data=sorted_data)

@app.route('/<username>')
def profile(username):
    user = User(username)
    timestamp_conversions = {}

    for timestamp in user.statuses | user.profile_pictures:
        timestamp_conversions[timestamp] = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d.%m.%Y %H:%M:%S')

    return render_template('profile.html', username=user.name, statuses = user.statuses, profile_pictures = user.profile_pictures , timestamp_conversions=timestamp_conversions)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')
    args = argparser.parse_args()
    if args.debug:
        app.run(debug=True)
    else:
        app.run()