# python-gsheets
Python Google Sheets Domain Processing

## Install basic python modules
pip3 install gspread
pip3 install import trafilatura
pip3 install import textstat
pip3 install import urllib
pip3 install import validators
pip3 install urlvalidator 

## Install Google Authentication
To use [gspread you need to use Google Sheets API](https://gspread.readthedocs.io/en/latest/oauth2.html) and be an authenticated user. This can be done in OAuth2 but I've used the basic authentication in ~/.config/gspread/service_account.json

Either way you'll need to get a project in [Google's Console set up](https://console.developers.google.com/project) to do this. I used my personal Google account.

This is a bot, so the [For Bots: Using Service Account](https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account) work great. 

I found making the spreadsheet editable with the link worked, I haven't dug into doing this with more restricted sheets. 

## TODO
* get proper URL parsing
 
