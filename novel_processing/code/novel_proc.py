# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 11:31:07 2016

@author: aliciagyori
"""

def imports():
    global pd
    import pandas as pd
    global np
    import numpy as np
    global TextBlob
    from textblob import TextBlob
    global csv
    import csv
    global load_etext
    from gutenberg.acquire import load_etext
    global strip_headers
    from gutenberg.cleanup import strip_headers
    global os
    import os
    
def csv_file(novel_num):
    novel = strip_headers(load_etext(novel_num))
    novel = novel.replace('\n', ' ')
    novel = TextBlob(novel)
    novel_sentences = novel.sentences
    m = str(novel_num)
    with open('../data/novel_'+m+'list_1.csv', 'wb') as f:
        writer = csv.writer(f)
        for sentence in novel_sentences:
            writer.writerow([sentence])
            
def CountSyllables(word, isName=True):
    vowels = "aeiouy"
    #single syllables in words like bread and lead, but split in names like Breanne and Adreann
    specials = ["ia","ea"] if isName else ["ia"]
    specials_except_end = ["ie","ya","es","ed"]  #seperate syllables unless ending the word
    currentWord = word.lower()
    numVowels = 0
    lastWasVowel = False
    last_letter = ""

    for letter in currentWord:
        if letter in vowels:
            #don't count diphthongs unless special cases
            combo = last_letter+letter
            if lastWasVowel and combo not in specials and combo not in specials_except_end:
                lastWasVowel = True
            else:
                numVowels += 1
                lastWasVowel = True
        else:
            lastWasVowel = False

        last_letter = letter

    #remove es & ed which are usually silent
    if len(currentWord) > 2 and currentWord[-2:] in specials_except_end:
        numVowels -= 1

    #remove silent single e, but not ee since it counted it before and we should be correct
    elif len(currentWord) > 2 and currentWord[-1:] == "e" and currentWord[-2:] != "ee" and currentWord != 'the':
        numVowels -= 1

    return numVowels            

def data_fr(novel_num):
    nn = str(novel_num)
    df_novel = pd.read_csv('../data/novel_'+nn+'list_1.csv', header=None)
    wrd_length = []
    total_char = []
    def wrd_char_counts(sentence):
        total_chars = 0
        wrd_counts = []
        for word in sentence:
            char_count = len(word)
            wrd_counts.append(char_count)
            total_chars += char_count
        total_char.append(total_chars)
        wrd_length.append(wrd_counts)
    for l in df_novel[0]:
        sent = TextBlob(l)
        wrd_char_counts(sent.words)   
    df_novel['wrd_length'] = wrd_length
    df_novel['total_char'] = total_char
    syl = []
    for l in df_novel[0]:
        sent = TextBlob(l)
        syl_single = []
        for x in sent.words:
            m = CountSyllables(x)
            syl_single.append(m)
        syl.append(syl_single)
    syl_count_arr = []
    for n in syl:
        n = np.array(n)
        syl_count_arr.append(n)
    df_novel['syl_count'] = syl_count_arr 
    d = {}
    for l in df_novel[0]:
        sent = TextBlob(l)
        for x in sent.words:
            w = CountSyllables(x)
            d[x] = w
    with open('../data/novel_'+nn+'list_1_syl.csv', 'wb') as f:
        writer = csv.writer(f)
        for row in d.iteritems():
            writer.writerow(row) 
    #create syllable sum column
    syl_sum = []
    for l in range(0,len(df_novel)):
        syl_sum.append(df_novel['syl_count'][l].sum()) 
    df_novel['syl_sum'] = syl_sum    
    df_novel.to_csv('../data/novel_'+nn+'list_1.csv', index=False)

imports()
data_fr(29728)
csv_file(29728)