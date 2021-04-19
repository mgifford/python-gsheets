# Pull in libraries
import gspread
import trafilatura
import textstat
import urllib
# import py-readability-metrics
# import readability.py

# from nltk.tokenize import sent_tokenize
# from readability import readability
# from readability.exceptions import ReadabilityException
# import json

# Connect Google account & URL
gc = gspread.service_account()
gspread_url = 'https://docs.google.com/spreadsheets/d/1EC42i2ETouRdQDJtF6guaS-3FIWSN6KUHs_ltdK-fV4/edit#gid=1129282989'
sh = gc.open_by_url(gspread_url)

# Fails on 4
for x in range(60, 1000):
#    print("We're on time %d" % (x))
    row = str(x)

    worksheet = sh.worksheet("data") # Get sheet by title
    val = worksheet.acell('A' + row).value # Get cell by label

    # Switch to the shell gsheet & add a url from the domain domain
    worksheet = sh.worksheet("shell") # By title
    url = "https://" + val

    def file_exists(url):
        request = urllib.Request(url)
        request.get_method = lambda : 'HEAD'
        try:
            response = urllib.urlopen(request)
            return True
        except urllib.HTTPError:
            url = "http://" + val
            return False

    # Test
    print(url)

    worksheet.update('A' + row, url)

    # Size of page in characters
    worksheet = sh.worksheet("shell") # By title
    downloaded = trafilatura.fetch_url(url)
    worksheet.update("B" + row, len(downloaded))
#    print(downloaded)
    if len(str(downloaded)) != 0:
        from readability.readability import Document
        from html2text import html2text

        readable_article = Document(downloaded).summary()

        raw = html2text(readable_article)
#        print(raw)
        worksheet = sh.worksheet("shell") # By title
        freading = textstat.flesch_reading_ease(raw)
        worksheet.update("C" + row, freading)

        worksheet = sh.worksheet("shell") # By title
        smog_index = textstat.smog_index(raw)
        worksheet.update("D" + row, smog_index)

        worksheet = sh.worksheet("shell") # By title
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(raw)
        worksheet.update("E" + row, flesch_kincaid_grade)

        worksheet = sh.worksheet("shell") # By title
        automated_readability_index = textstat.automated_readability_index(raw)
        worksheet.update("F" + row, automated_readability_index)

#        print(freading)
