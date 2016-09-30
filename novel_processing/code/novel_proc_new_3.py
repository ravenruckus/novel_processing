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
    global KMeans
    from sklearn.cluster import KMeans
    global StandardScaler
    from sklearn.preprocessing import StandardScaler
    global re
    import re
    
#pulls in novel number from gutenberg and trys to assign the novel text to the 
#variable novel. If it can't it returns the nobel numbers     
def to_text(novel_num):
    novel_num = int(novel_num)
    global novel
    novel = None
    try:
        novel = load_etext(novel_num)
        return True
    except:
        return novel_num
#the novel text and number are run through this function. If the novel has
#ASCII encoding then it is stripped of it's headers and put into sentences &
# a csv file is created and the function returns true. Or the function returns false
#so that the novel number can be put into a reject list        
def csv_file(novel, novel_num):
    if re.search('Character set encoding: ASCII', novel):
        novel = strip_headers(novel)
        novel = novel.replace('\n', ' ')
        novel = TextBlob(novel)
        novel_sentences = novel.sentences
        m = str(novel_num)
        with open('../data/novel_'+m+'list_1.csv', 'wb') as f:
            writer = csv.writer(f)
            for sentence in novel_sentences:
                writer.writerow([sentence])
        return True              
    else: 
        return False

#each word in a sentence is passed through and the syllables are counted       
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
#gets the length of each word in a sentence and creates a coloumn of lists
def wrd_lengths(sentence):
    return [len(word) for word in TextBlob(sentence).words]
#runs the syllable count function on each sentence and creates a column of lists
def  syl_count(sentence):
    return[CountSyllables(l) for l in TextBlob(sentence).words] 
def detect_sentiment(text):
    return TextBlob(text.decode('utf-8')).sentiment.polarity    

         
#takes the novel text and novel number. If a csv file was created then the code 
# is run other wise the number goes into the second reject list. if the code is
# run then the wrd_length, total_char, syl_count, syl_sum, and cluster colomns
# are attempted to be created & then added to the csv file. If this cannot happen
# then the number is added to the third reject list. & a syllable to word count
# csv file is made for each funcitoning number
def data_fr(novel, novel_num):
    if csv_file(novel, novel_num) is True:
        nn = str(novel_num)
        df_novel = pd.read_csv('../data/novel_'+nn+'list_1.csv', header=None)
        try: 
            df_novel['wrd_length'] = df_novel[0].apply(wrd_lengths)
            df_novel['total_char'] = [sum(l) for l in df_novel['wrd_length']]
            df_novel['syl_count'] = df_novel[0].apply(syl_count)
            df_novel['syl_sum'] = [sum(l) for l in df_novel['syl_count']]
            df_novel['sentiment'] = df_novel[0].apply(detect_sentiment)
            #create csv for word to syl to improve syl function
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
            #create cluster columns
            df_cluster = df_novel.drop('wrd_length', 1)
            df_cluster = df_cluster.drop('syl_count', 1)
            X = df_cluster.drop(0, axis = 1)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            km = KMeans(n_clusters=20, random_state=1)
            km.fit(X_scaled)
            df_cluster_20 = df_cluster.copy()
            df_cluster_20['cluster'] = km.labels_
            df_novel['cluster_20'] = df_cluster_20['cluster']
            #Create cluster 3
            df_cluster_3 = df_cluster.copy()
            X = df_cluster_3.drop(0, axis=1)
            X_scaled = scaler.fit_transform(X)
            km = KMeans(n_clusters = 3, random_state=1)
            km.fit(X_scaled)
            df_cluster_3['cluster'] = km.labels_
            df_novel['cluster_3_syl'] = df_cluster_3['cluster']
            #create cluster 3 no syl
            df_cluster_3no_syl = df_cluster.copy()
            X = df_cluster_3no_syl.drop(0, axis=1)
            X_scaled = scaler.fit_transform(X)
            km = KMeans(n_clusters=3, random_state=1)
            km.fit(X_scaled)
            df_cluster_3no_syl['cluster'] = km.labels_
            df_novel['cluster_3no_syl'] = df_cluster_3no_syl['cluster']
            #Create 5 clusters
            df_cluster_5 = df_cluster.copy()
            X = df_cluster_5.drop(0, axis=1)
            X_scaled = scaler.fit_transform(X)
            km = KMeans(n_clusters=5, random_state=1)
            km.fit(X_scaled)
            df_cluster_5['cluster'] = km.labels_
            df_novel['cluster_5'] = df_cluster_5['cluster']
            df_novel.to_csv('../data/novel_'+nn+'list_1.csv', index=False)
        except:
            rejects_3.append(novel_num)
    else:
        rejects_2.append(novel_num)
        
def test_func(novel_number):
    global rejects
    global rejects_2 
    global rejects_3
    rejects = []
    rejects_2 = []
    rejects_3 = []
    if to_text(novel_number) != True:
        w = None
        w = to_text(novel_number)
        rejects.append(w)
    else:
        data_fr(novel, novel_number)
            
        
#Main Function. Creates the three reject lists, opens the list file and 
#loops the list through the to_text function. If the to_text function is trus 
# then the novel is run through the data_fr function else the novel_num is 
#appended to the first reject list
def novels():
    global rejects
    global rejects_2 
    global rejects_3
    rejects = []
    rejects_2 = []
    rejects_3 = []
    global c
    c = 0
    with open('../data/list_1.csv', 'r') as csvfile:
        listreader = csv.reader(csvfile.read().splitlines())
        for row in listreader:
            nv = row[0]
            if to_text(nv) != True:
                w = None
                w = to_text(nv)
                rejects.append(w)
            else:
                data_fr(novel, nv)
            c += 1
    rejects_csv()            
            
def rejects_csv():        
   with open('../data/rejects.csv', 'wb') as f:
       writer = csv.writer(f)
       for l in rejects:
           writer.writerow([l])
                
   with open('../data/rejects_2.csv', 'wb') as f:
       writer = csv.writer(f)
       for l in rejects_2:
           writer.writerow([l])
           
   with open('../data/rejects_3.csv', 'wb') as f:
       writer = csv.writer(f)
       for l in rejects_3:
           writer.writerow([l])
       

imports()
novels()
