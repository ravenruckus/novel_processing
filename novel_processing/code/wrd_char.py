# -*- coding: utf-8 -*-
"""
Created on Mon May 16 13:30:21 2016

@author: aliciagyori
"""

def wrd_char(novel_title):
    import pandas as pd
    from textblob import TextBlob
    df_novel = pd.read_csv('../data/novel_' + novel_title + '3.csv', index_col=False) 
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
        
    for l in df_novel['0']:
        sent = TextBlob(l)
        wrd_char_counts(sent.words)
    df_novel['wrd_length'] = wrd_length
    df_novel['char_length'] = total_char 
    df_novel.to_csv('../data/novel_' + novel_title + '3.csv', index=False)    
        
    return (wrd_length, total_char)

    
#wrd_length, total_char = wrd_char('wizard')
#df_novel = pd.read_csv('../data/novel_' + 'wizard' + '3.csv', index_col=False) 