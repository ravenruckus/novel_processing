# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:51:27 2016

@author: aliciagyori
"""

import pandas as pd
import csv 
import numpy as np
#cycle through percentage, find the mean of first 19, find the difference between
#last and mean. divide that by mean and add to a list. then do that for the next
#novel. find mean of all novels for that percentage
#go to next percentage and do same thing 
#compare means of all percentage to find the smallest percentage



def find_this(df, t, x):
    ratio = (df['total_char'].sum()/3) - (.02 * (int(len(df) - 1)))
    w = 0
    sent_stop = []
    while w <= ratio:
        w = df['total_char'][t:x].sum()
        sent_stop.append(x)
        x += 1
    return max(sent_stop)


def start_stop(df):    
    #nn = str(x)
    #df = pd.read_csv('novel_'+nn+'list_1.csv') 
    t = 0
    x = 0
    start_point = []
    stop_point = []
    for n in range(1,3):
        s = find_this(df, t, x)
        start_point.append(t)
        stop_point.append(s)
        t = s
        x = s + 1
    start_point.append(stop_point[1]) 
    stop_point.append(len(df))
    return start_point, stop_point
    
#creates the reject_list by cycling through all of the reject lists    
def reject_list():
    main_rejects = []
    with open('list_1_rejects.csv') as csvfile:
        listreader = csv.reader(csvfile.read().splitlines())
        for row in listreader:
            main_rejects.append(row[0])
    with open('list_1_rejects_2.csv') as csvfile:
        listreader = csv.reader(csvfile.read().splitlines())
        for row in listreader:
            main_rejects.append(row[0])
    with open('list_1_rejects_3.csv') as csvfile:
        listreader = csv.reader(csvfile.read().splitlines())
        for row in listreader:
            main_rejects.append(row[0])
    return main_rejects  
#creats the main list by adding all of the novels to main_list that are not in 
#the reject list    
def main_list():
    main_list = []
    reject_li = reject_list()
    with open('list_1.csv', 'r') as csvfile:
        listreader = csv.reader(csvfile.read().splitlines())
        for row in listreader:
            nv = row[0]
            if nv in reject_li:
                pass
            else:
                main_list.append(nv)
    return main_list
        
#finds     
def total_char_sum(novel_num):
    nn = str(novel_num)
    df = pd.read_csv('novel_'+nn+'list_1.csv') 
    three_pieces = []
    start_point, stop_point = start_stop(df)
    for l in range(0,3):
        sr = start_point[l]
        st = stop_point[l]
        r = df['sentiment'][sr:st].mean()
        three_pieces.append(r) 
    return three_pieces    

def to_csv(novel_num):
    three_pieces = total_char_sum(novel_num)
    three_pieces.insert(0,novel_num)
    with open('three_pieces.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(three_pieces)     
#cyles through all of the novels that are not on the reject list and have dataframes 
    #and finds the perc differance between the first 19 and the last piece of each
    #novel for a particular percentage point

def main():
        main_li = main_list()
        for l in main_li:
            to_csv(l)
            #twenty_pieces = total_char_sum(l)
            #print twenty_pieces
            

   
 
#.02 seems to help the most    