# MUW announcement Checker

Checks new announcements on MUW page and send them to Telegram chat


Clone repo and go to the folder
```
git clone https://github.com/prianichnikov/muw_announces_checker

cd muw_announces_checker
```

Install Python 3 and pip
```
sudo apt install python3 python3-pip
```

Install required python modules
```
pip3 install -r requirements.txt
```

Set your own Telegram bot token and chat id
```
TG_BOT_TOKEN=...
TG_CHAT_ID=...
```

Finally, add checker into crontab
```
crontab -e 

3 8-20 * * 1-5 <PATH_TO_FOLDER>/muw_announces_checker/muw_announces_checker.py >> /tmp/muw_checker.log

crontab -l
```