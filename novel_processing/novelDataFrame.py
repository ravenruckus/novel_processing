# -*- coding: utf-8 -*-
"""
Created on Fri May 13 15:51:55 2016

@author: aliciagyori
"""

import pandas as pd
from textblob import TextBlob
import csv
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
def novel(n,t,s):
    #dependant on textblob, csv, from gutenberg.acquire import load_etext, 
    #from gutenberg.cleanup import strip_headers
    novel = strip_headers(load_etext(n))
    novel = novel.replace('\n', ' ')
    novel = TextBlob(novel)
    novel_sentences = novel.sentences
    novel_title = t
    for l in range(2):
        novelWriter = csv.writer(open('novel_' + novel_title + '.csv', 'w'), delimiter=',')
        for sentence in novel_sentences:
            novelWriter.writerow([sentence])
    df_novel = pd.read_csv('novel_' + novel_title + '.csv', skiprows = s, header=None)
    df_novel.rename(columns={0:'Sentences'}, inplace=True)

    #run loop on def wrd_char_counts & add lists to dataframe
    #run loop on syl & add to data from. & create a csv file for the syl
    #sentiment column
    wrd_length = []
    total_char = []
    def wrd_char_counts(sentence):
        total_chars = 0 #characters in the sentence
        wrd_counts = [] # number of char per word in sentence
        for word in sentence:
            wrd = word
            char_count = len(wrd)
            wrd_counts.append(char_count)
            total_chars += char_count
        total_char.append(total_chars)
        wrd_length.append(wrd_counts)
    
    for l in df_novel['Sentences']:
        sent = TextBlob(l)
        wrd_char_counts(sent.words)
    df_novel['wrd_length'] = wrd_length
    df_novel['char_total'] = total_char
    df_novel.to_csv('novel_' + novel_title + '.csv') 
    return df_novel.head()
    print total_char
    





    
    
    