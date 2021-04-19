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

print(cfg.gspread_url)

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
#        print(downloaded)

#    print(downloaded)
    if url != 0 and downloaded:
        from readability.readability import Document
        from html2text import html2text

        readable_article = Document(downloaded).summary()

        raw = html2text(readable_article)
        print(raw)

        # Lexicon Count - number of words present in the text
        lexicon_count = textstat.lexicon_count(raw, removepunct=True)
        worksheet.update("C" + row, lexicon_count)

        # Sentence Count
        sentence_count = textstat.sentence_count(raw)
        worksheet.update("D" + row, sentence_count)

        # The Flesch Reading Ease formula
        # 90-100 - Very Easy | 80-89 - Easy | 70-79 - Fairly Easy | 60-69 - Standard
        # 50-59 - Fairly Difficult | 30-49 - Difficult | 0-29 - Very Confusing
        flesch_reading_ease = textstat.flesch_reading_ease(raw)
        worksheet.update("E" + row, flesch_reading_ease)

        # Flesch-Kincaid Grade Level
        # https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#Flesch%E2%80%93Kincaid_grade_level
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(raw)
        worksheet.update("F" + row, flesch_kincaid_grade)

        # The Fog Scale (Gunning FOG Formula)
        # https://en.wikipedia.org/wiki/Gunning_fog_index
        gunning_fog = textstat.gunning_fog(raw)
        worksheet.update("G" + row, gunning_fog)

        # The SMOG Index
        # https://en.wikipedia.org/wiki/SMOG
        smog_index = textstat.smog_index(raw)
        worksheet.update("H" + row, smog_index)

        # Automated Readability Index
        # https://en.wikipedia.org/wiki/Automated_readability_index
        automated_readability_index = textstat.automated_readability_index(raw)
        worksheet.update("I" + row, automated_readability_index)

        # The Coleman-Liau Index
        # https://en.wikipedia.org/wiki/Coleman%E2%80%93Liau_index
        coleman_liau_index = textstat.coleman_liau_index(raw)
        worksheet.update("J" + row, coleman_liau_index)

        # Linsear Write Formula
        # https://en.wikipedia.org/wiki/Linsear_Write
        linsear_write_formula = textstat.linsear_write_formula(raw)
        worksheet.update("K" + row, linsear_write_formula)

        # Dale-Chall Readability Score
        # < 4.9 - average 4th-grade student | 5.0–5.9 - average 5th or 6th-grade
        # 6.0–6.9 - average 7th or 8th-grade | 7.0–7.9 - average 9th or 10th-grade
        # 8.0–8.9	average 11th or 12th-grade | 9.0–9.9 - college student
        dale_chall_readability_score = textstat.dale_chall_readability_score(raw)
        worksheet.update("L" + row, dale_chall_readability_score)

        # Readability Consensus based upon all the above tests
        # Estimated school grade level required to understand the text
        text_standard = textstat.text_standard(raw, float_output=False)
        worksheet.update("M" + row, text_standard)
