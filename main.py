"""
encoding: utf-8
"""
from __future__ import division
from goose import Goose
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import urllib2
import math


class Summarizer(object):
    def sentence_intersection(self, sent1, sent2):
        sent1_tokens = [ w for w in word_tokenize(sent1) if w not in
                        stopwords.words('english')]
        sent2_tokens = [ w for w in word_tokenize(sent2) if w not in
                        stopwords.words('english')]

        normal = math.log(len(sent1_tokens) + len(sent2_tokens))

        return len(set(sent1_tokens).intersection(sent2_tokens)) / normal

    def rank_sentences(self, sentences):
        n = len(sentences)
        print sentences[0][0]
        score =  [0 for x in xrange(n)]

        for i in range(0, n):
            for j in range(0, n):
                score[i] += self.sentence_intersection(
                    sentences[i],     
                    sentences[j])
        return score




    def summarize(self, text):
        sentences = sent_tokenize(text)
        scores = self.rank_sentences(sentences)
        sorted_scores = sorted(enumerate(scores), reverse=True,
                               key=lambda x:x[1])
        print "Original Length: ", len(sentences)
        sum_length = int(len(sentences) * 0.25)
        print "New Length: ", sum_length
        ranked_sentences = sorted(sorted_scores[:sum_length],
                                   key=lambda x:x[0])
        return [sentences[index] for index, _ in
                ranked_sentences]
    

def get_text(article_url):
    goose = Goose()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(article_url)
    raw_html = response.read()
    article = goose.extract(raw_html=raw_html)
    return article.cleaned_text

def main():
    summarizer = Summarizer()
    article_url = raw_input('Enter a url: ')

    print summarizer.summarize(get_text(article_url))

if __name__ == "__main__":
    main()

