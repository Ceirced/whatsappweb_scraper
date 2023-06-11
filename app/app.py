from flask import Flask, render_template
import os
import json
from collections import OrderedDict
import datetime

app = Flask(__name__)

@app.route('/')
def index():

    directory = '/home/cederic/whatsappweb_scraper'
    # Define the root directory where your subfolders are located
    root_directory = f'{directory}/profile_pictures'

    # Get a list of all subfolders
    subfolders = [folder for folder in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, folder))]

    # Create an empty dictionary to store the data
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