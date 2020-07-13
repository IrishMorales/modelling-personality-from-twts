# -*- coding: utf-8 -*-
#PY2 SCRIPT FOR PREPROCESSING
import csv
import ftfy
import io
import re
import emoji
import tweetokenize.tokenizer
from tweetokenize import Tokenizer


#function to replace emoticons with "EMOTICON"
def tokenize_emoticon(text):
    #store emoticons in list
    with open('emoticons.txt', 'r') as f:
        emoticons = [unicode(line.strip().decode('utf-8')) for line in f]

        for i in range(len(text)):
            if text[i] in emoticons:
                text[i] = u"EMOTICON"

        return text

    
#function to replace other broken encoding
def fix_other(text):
    for i in range(len(text)):
        if (text[i] == u'\u2014' or text[i] == u'\u2013'):
            text[i] = "-"
        if (text[i].find(u'\u2026') or text[i] == u'\u2026'):
            text[i] = text[i].replace(u"\u2026","...")
    return text


#configure tweetokenize Tokenizer
tknzr = Tokenizer(lowercase = False,
                  allcapskeep = True,
                  normalize = False,
                  usernames = 'USERNAME',
                  urls = 'URL',
                  hashtags = 'HASHTAG',
                  ignorequotes = False,
                  ignorestopwords = False)
                  
tknzr.emoticons(filename="emoticons.txt")


#input and output filepaths
#pretoken_filepath = 'practice-data/tweet_tweet.csv'
pretoken_filepath = 'project-data/twitter_tweet.csv'
posttoken_filepath = 'preprocessed-data/tweet_tweet_pp.csv'
text_index = 3


#read from input, tokenize, write to output
with io.open(pretoken_filepath, 'rb') as infile, open(posttoken_filepath, 'wb') as outfile:
    reader = csv.reader(infile,
                        delimiter=",")
    writer = csv.writer(outfile,
                        delimiter=";",
                        quotechar='"',
                        quoting=csv.QUOTE_ALL,
                        escapechar='')
        
    #write header
    writer.writerow(next(reader))

    #tokenize text by tweet
    for row in reader:
        #remove line breaks (LF) inside tweets
        row[text_index]=re.sub(r'(?<!")\n', '', row[text_index])
        #decode to bytes ex. /xf3/xf2
        row[text_index]=row[text_index].decode('utf-8')
        #fix with ftfy
        row[text_index]=ftfy.fix_text(row[text_index], fix_line_breaks=False, fix_surrogates=False)
        #change emojis to EMOJI
        row[text_index]=emoji.demojize(row[text_index])
        #encode back to utf-8
        row[text_index]=row[text_index].encode('utf-8')
        #tokenization functions
        row[text_index]=tknzr.tokenize(row[text_index])
        row[text_index]=tokenize_emoticon(row[text_index])
        row[text_index]=fix_other(row[text_index])

        writer.writerow(row)
