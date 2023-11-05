# whatsappweb_scraper

## description
This python script uses selenium to download and check for new profile pictures of whatsapp contacts.
It uses the chrome browser and chromedriver to run. 
It uses the `users.json` file to get the names of the users to check. 
It will create a folder for each user and save the profile pictures in it.

## requirements
+ python
+ selenium library
+ chrome Browser and chromedriver
+ whatsapp web
+ file called `users.json` with the following format:
```
{
    "users": [
        {
            "name": "user1",
        },
        {
            "name": "user2",
        }
    ]
}
```
where `name` is the how the user is displayed in whatsapp web i.e. how you saved the contact in your phone.

Linux:
```
./main.py 
```

## options

+ `--head` : run the browser in head mode
+ `-t, --time` : time to wait for whatsapp to log in (default 30 seconds)
+ `-u, --user` : scrape a specific user

## to run the dockerimage
UID und GID are set in the ~/.bashrc file with
```
export UID=$(id -u)
export GID=$(id -g)
```

in bash:
```
docker build -t selenium_docker . --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)
docker compose up -f scrape_container_docker-compose.yml up
```