#!/usr/bin/env python

# Pull in libraries
import gspread
import trafilatura
import textstat
import urllib
import validators

import setup as cfg

# import py-readability-metrics
# import readability.py

# from nltk.tokenize import sent_tokenize
# from readability import readability
# from readability.exceptions import ReadabilityException
# import json

# Connect Google account & URL
gc = gspread.service_account()
# gspread_url = 'https://docs.google.com/spreadsheets/d/1EC42i2ETouRdQDJtF6guaS-3FIWSN6KUHs_ltdK-fV4/edit#gid=1129282989'
gspread_url = cfg.gspread_url
sh = gc.open_by_url(gspread_url)

# Fails on 64
for x in range(cfg.start, cfg.end):
#    print("We're on time %d" % (x))
    row = str(x)

    worksheet = sh.worksheet("data") # Get sheet by title
    val = worksheet.acell('A' + row).value # Get cell by label

    # Switch to the shell gsheet & add a url from the domain domain
    worksheet = sh.worksheet("shell") # By title

    from urlvalidator import validate_url, validate_email, ValidationError
    url = 0
    try:
       validate_url("https://" + val)
       url = "https://" + val
    except ValidationError:
       raise ValidationError("Invalid URL")

    # if validators.domain("http://" + val):
    #     url = "http://" + val
    # elif validators.domain("http://www." + val):
    #    url = "http://www." + val

    # print(validators.domain("https://" + val))

    # Test
    print(url)

    if url != 0:
        worksheet.update('A' + row, url)

        # Size of page in characters
        worksheet = sh.worksheet("shell") # By title
        downloaded = trafilatura.fetch_url(url)
        worksheet.update("B" + row, len(str(downloaded)))

#    print(downloaded)
    if url != 0 or len(str(downloaded)) != 0:
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
