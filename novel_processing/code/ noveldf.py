# -*- coding: utf-8 -*-
"""
Created on Mon May 16 13:05:59 2016

@author: aliciagyori
"""

def novelDF(n,t):
    from textblob import TextBlob
    import csv
    from gutenberg.acquire import load_etext
    from gutenberg.cleanup import strip_headers
    novel = strip_headers(load_etext(n))
    novel = novel.replace('\n', ' ')
    novel = TextBlob(novel)
    novel_sentences = novel.sentences
    novel_title = t
    for l in range(2):
        novelWriter = csv.writer(open('../data/novel_'+ novel_title + '3.csv', 'w'), delimiter=',')
        for sentence in novel_sentences:
            novelWriter.writerow([sentence])
    #df_novel = pd.read_csv('../data/novel_' + novel_title + '3.csv', skiprows = s, header = None)        
    #df_novel.rename(columns={0:'Sentences'}, inplace=True)
    #for l in range(2):
        #df_novel.to_csv('../data/novel_' + novel_title + '3.csv', index=False)
    return novel_title
    
    
#import pandas as pd    
#df_novel = pd.read_csv('../data/novel_' + 'wizard' + '3.csv', header=None, index_col=False)    
    
def wrd_char(novel_title):
    import pandas as pd
    from textblob import TextBlob
    df_novel = pd.read_csv('../data/novel_' + novel_title + '3.csv', header=None, index_col=False) 
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
    df_novel['char_length'] = total_char 
    df_novel.to_csv('../data/novel_' + novel_title + '3.csv', index=False)    
        
 
novel_title = novelDF(55, 'wizard')
x , y = wrd_char(novel_title)   

#try going through 2 or 3 spots in the key
#read in key & then 
import pandas as pd
key = pd.read_csv('../data/novel_key.csv')

for l in range(0,3):
    n = key['novel_num'][int(l)]
    t = key['Title'][int(l)]
    novel_title=novelDF(n,t)
    wrd_char(novel_title)

#run draft again to see what a graft looks like when getting the syll sum
#is there another way to graft those sentences? 
#and then when putting that into 20 pieces and then maybe 100 pieces
    
#change novel_title to novel_number
#add syl count, with making csv for syll to word.
#clean up folders
#go through list and remove unwanted items     
#run all of the novels 
   