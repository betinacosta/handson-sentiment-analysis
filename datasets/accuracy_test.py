# -*- coding: utf-8 -*-

from textblob import TextBlob

def positive_analysis():
    count = 0
    correct = 0
    with open("datasets/positive.txt","r") as f:
        for line in f.read().split('\n'):
            analysis = TextBlob(line)
            if analysis.sentiment.polarity > 0:
                correct += 1
            count +=1
            
    print("Positive accuracy = {}% via {} samples".format(correct/count*100.0, count))

def negative_analysis():
    count = 0
    correct = 0
    with open("datasets/negative.txt","r") as f:
        for line in f.read().split('\n'):
            analysis = TextBlob(line)
            if analysis.sentiment.polarity < 0:
                correct += 1
            count +=1
            
    print("Negative accuracy = {}% via {} samples".format(correct/count*100.0, count))
    
positive_analysis()
negative_analysis()
