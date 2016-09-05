# InstaPromoter

A simple Instagram bot that pulls trending top hashtags and auto likes pictures with those hashtags to get more followers.

##Setup
Clone this repository:
```
git clone https://github.com/Pogorelov/InstaPromoter.git
```
run the following command to install the required libraries:
```
sudo pip install -r requirements.txt
```


Modify the InstaPromoterProfile.yml file to include your personal information. You can fill unlimited number of accounts and just specify the number of account in the run command.
```
INSTAGRAM1:  #account number - 1
  USERNAME1: #YOUR_INSTAGRAM_USERNAME
  PASSWORD1: #YOUR_INSTAGRAM_PASSWORD
CREDENTIALS1:
  CODE1: #Instagram provides a code for you in https://www.instagram.com/developer
  CLIENT_ID1: #Instagram provides a cliend_id for you in https://www.instagram.com/developer
  REDIRECT_URL1: #https://www.instagram.com/YOUR_INSTAGRAM_USERNAME
INSTAGRAM2:   #account number - 2
  USERNAME2:  #YOUR_INSTAGRAM_USERNAME
  PASSWORD2:  #YOUR_INSTAGRAM_PASSWORD
CREDENTIALS2:
...
SLEEPTIME: 10
PER_HASHTAG: 20 (Number of media posts for one hashtag)
MAX_HASHTAGS: 10 (Number of top hashtags)
HOT_HASHTAGS: True (True - top hashtags, False - read the file hashtags.txt)
```

Run:
```
py InstaPromoter_v2.py {account_number}
```

LinkedIn: https://www.linkedin.com/in/pogorelovmaxim

Facebook: https://www.facebook.com/Pogorelov23
