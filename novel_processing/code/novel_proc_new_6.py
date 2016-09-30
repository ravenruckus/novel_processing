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
    
class Text(object):
    def __init__(self, novel_num):
        self.novel_num = int(novel_num)
               
    def the_text(self): 
         try:
            self.novel = load_etext(self.novel_num)
         except:
            rejects.append(self.novel_num)
            return False
              
         if re.search('Character set encoding: ASCII', self.novel):
            self.novel = strip_headers(self.novel)
            self.novel = self.novel.replace('\n', ' ')
            self.novel = TextBlob(self.novel)
            self.novel_sentences = self.novel.sentences
            self.m = str(self.novel_num)
            with open('novel_'+self.m +'list_1.csv', 'wb') as f:
                writer = csv.writer(f)
                for sentence in self.novel_sentences:
                    writer.writerow([sentence])
         else: 
            rejects_2.append(self.novel_num) 
            return False    
#pulls in novel number from gutenberg and trys to assign the novel text to the 
#variable novel. If it can't it returns the nobel numbers     

#the novel text and number are run through this function. If the novel has
#ASCII encoding then it is stripped of it's headers and put into sentences &
# a csv file is created and the function returns true. Or the function returns false
#so that the novel number can be put into a reject list        


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

def find_this(df_novel, t,x):
    w = 0
    sent_stop = []
    while w <= ratio:
        w = df_novel['total_char'][t:x].sum()
        sent_stop.append(x)
        x += 1
    return max(sent_stop)
def twenty_pieces(df_novel):
    t = 0
    x = 0
    global ratio
    ratio = (df_novel['total_char'].sum()/20) - (.06 * (int(len(df_novel) - 1)))
    start_point = []
    stop_point = []
    for n in range(1,21):
        s = find_this(df_novel, t, x)
        start_point.append(t)
        stop_point.append(s)
        t = s
        x = s + 1
    return start_point, stop_point         
#takes the novel text and novel number. If a csv file was created then the code 
# is run other wise the number goes into the second reject list. if the code is
# run then the wrd_length, total_char, syl_count, syl_sum, and cluster colomns
# are attempted to be created & then added to the csv file. If this cannot happen
# then the number is added to the third reject list. & a syllable to word count
# csv file is made for each funcitoning number
def data_fr(novel_num):
    #if csv_file(novel, novel_num) is True:
    nn = str(novel_num)
    df_novel = pd.read_csv('novel_'+nn+'list_1.csv', header=None)
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
        with open('novel_'+nn+'list_1_syl.csv', 'wb') as f:
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
        df_novel.to_csv('novel_'+nn+'list_1.csv', index=False)
        start_point, stop_point = twenty_pieces(df_novel)
        st = 0
        for l in start_point:
            strt = start_point[st]
            stp = stop_point[st]
            mn = df_novel['sentiment'][strt:stp].mean()
            twenty_piece_char.append(mn)
            st += 1
        
        twenty_piece_char.insert(0,novel_num)
        with open('twenty_piece_test_3.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(twenty_piece_char)
    except:
        rejects_3.append(novel_num)
 


def rejects_csv():        
   with open('list_1_rejects.csv', 'wb') as f:
       writer = csv.writer(f)
       for l in rejects:
           writer.writerow([l])
                
   with open('list_1_rejects_2.csv', 'wb') as f:
       writer = csv.writer(f)
       for l in rejects_2:
           writer.writerow([l])
           
   with open('list_1_rejects_3.csv', 'wb') as f:
       writer = csv.writer(f)
       for l in rejects_3:
           writer.writerow([l])
            
        
#Main Function. Creates the three reject lists, opens the list file and 
#loops the list through the to_text function. If the to_text function is true 
# then the novel is run through the data_fr function else the novel_num is 
#appended to the first reject list
def novels():
    global rejects
    global rejects_2 
    global rejects_3
    global twenty_piece_char 
    rejects = []
    rejects_2 = []
    rejects_3 = []
    global c
    c = 0
    imports()
    with open('list_1.csv', 'r') as csvfile:
        listreader = csv.reader(csvfile.read().splitlines())
        for row in listreader:
            twenty_piece_char = []
            nv = row[0]
            x = Text(nv)
            x.the_text()  
            
            if x.novel_num in rejects or x.novel_num in rejects_2:
                pass
            else:
              data_fr(x.novel_num)  
            c += 1   
    
    rejects_csv()
    
novels()    


def test(test_nov):
    global rejects
    global rejects_2 
    global rejects_3
    global twenty_piece_char 
    twenty_piece_char = []
    rejects = []
    rejects_2 = []
    rejects_3 = []
    global c
    imports()
    nv = test_nov
    x = Text(nv)
    x.the_text()
    if x.novel_num in rejects or x.novel_num in rejects_2:
        pass
    else:
        data_fr(x.novel_num)
    print twenty_piece_char    
    
n = [55, 76,1342, 11 ]
for l in n:
    test(l)   
    
    
test(55)    
    

    
    


