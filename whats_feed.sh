#!/bin/bash

source $HOME/whatsappweb_scraper/env/bin/activate

flask --app $HOME/whatsappweb_scraper/app/app run --port=5040 &
sleep 0.5

SERVER_PID=$!



firefox -new-tab http://localhost:5040

echo Server PID: $SERVER_PID

read -p "Press any key to stop... " -r


kill $SERVER_PID

