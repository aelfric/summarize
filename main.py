"""
encoding: utf-8
"""
from __future__ import division
from goose import Goose
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
import urllib2
import math


class Summarizer(object):
    def sentence_intersection(self, sent1, sent2):
        normal = math.log(len(sent1) + len(sent2))

        return len(set(sent1).intersection(sent2)) / normal

    def rank_sentences(self, sentences):
        n = len(sentences)
        score =  [0 for x in xrange(n)]

        for i in range(0, n):
            for j in range(0, n):
                score[i] += self.sentence_intersection(
                    sentences[i],     
                    sentences[j])
        return score

    def __init__(self, text):
        self.text = text
        self.sentences = sent_tokenize(text)
        self.tokenized_sentences = [
            [w for w in word_tokenize(sent) if w not in
             stopwords.words('english') ] 
            for sent in self.sentences]


    def summarize(self, factor=0.4):
        scores = self.rank_sentences(self.tokenized_sentences)
        sorted_scores = sorted(enumerate(scores), reverse=True,
                               key=lambda x:x[1])

        sum_length = int(len(self.sentences) * factor)
        
        return [self.sentences[index] for index, _ in
                sorted(sorted_scores[:sum_length],
                                   key=lambda x:x[0])]
    
    def extract_keywords(self):
        pos_tagged_sents = [pos_tag(sent) 
                            for sent in self.tokenized_sentences]

        words = [ (w, pos) for sent in pos_tagged_sents for w, pos in sent]
        
        graph = {}

        for index, (word, pos) in enumerate(words):
            if pos in ['NN', 'NNS', 'NNPS', 'NNP']:
                start = max(0, index-2)
                end = min(index+2, len(words))
                graph[word] = ":".join([w for w, pos in words[start:end]])

        keyword_candidates = graph.items()
        return keyword_candidates
    
def get_text(article_url):
    goose = Goose()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(article_url)
    raw_html = response.read()
    article = goose.extract(raw_html=raw_html)
    return article.cleaned_text

def main():
    article_url = raw_input('Enter a url: ')
    summarizer = Summarizer(get_text(article_url))

    print summarizer.summarize()
    print summarizer.extract_keywords()

if __name__ == "__main__":
    main()

