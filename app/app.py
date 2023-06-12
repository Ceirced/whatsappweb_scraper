from flask import Flask, render_template
import os
import json
from collections import OrderedDict
import datetime
import sys
import os

# Get the absolute path of the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(parent_dir)

# Append the parent directory to sys.path
sys.path.append(parent_dir)

from user import User

app = Flask(__name__)

directory = '/home/cederic/whatsappweb_scraper'
root_directory = f'{directory}/profile_pictures'
subfolders = [folder for folder in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, folder))]

@app.route('/')
def index():

    data = {}

    for folder in subfolders:
        user = User(folder)
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
                    'timestamp': timestamp,
                    'timestamp_human': datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'),
                    'status': '',
                    'picture_id': picture
                }
    sorted_data = sorted(data.items(), key=lambda x: x[1]['timestamp'], reverse=True)

    return render_template('feed.html', data=sorted_data)


@app.route('/by_name')
def by_name():

    data = {}

    # Iterate over each subfolder
    for folder in subfolders:
        # Read the JSON file in each subfolder
        json_file = os.path.join(root_directory, folder, f'{folder}.json')
        with open(json_file) as f:
            folder_data = json.load(f, object_pairs_hook=OrderedDict)

        # Extract the name, statuses, and profile pictures from the JSON data
        name = folder_data['name']
        statuses = folder_data['statuses']
        profile_pictures = folder_data['profile_pictures']

        unique_profile_pictures = {}
        unique_values = set()

        for timestamp, picture in profile_pictures.items():
            if picture not in unique_profile_pictures.values():
                unique_profile_pictures[timestamp] = picture
                unique_values.add(picture)


        combined_data = []

        # Merge statuses and profile pictures based on timestamps
        timestamps = set(statuses.keys()) | set(unique_profile_pictures.keys())
        # timestamps = [int(timestamp) for timestamp in timestamps]
        for timestamp in sorted(timestamps,reverse=True):
            status = statuses.get(timestamp, '')
            picture_path = profile_pictures.get(timestamp, '')

            combined_data.append({
                'timestamp': timestamp,
                'timestamp_human': datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'),
                'status': status,
                'picture_path': picture_path
            })

        data[name] = combined_data
    # Render the template with the data
    return render_template(f'index.html', data=data, root_directory=root_directory)



if __name__ == '__main__':
    app.run()