# -*- coding: utf-8 -*-
#
from flask import Flask, request, render_template
from main import Summarizer, get_text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("demo.html")

@app.route('/test')
def test():
    s = Summarizer()
    text = get_text('http://www.techtimes.com/articles/60808/20150616/xbox-one-backward-compatibility-heres-an-initial-list-of-xbox-360-games-you-can-play.htm')
    return "\n".join(s.summarize())

@app.route('/demo', methods=['POST'])
def demo():
    text = request.form["text"]
    summ_len = float(request.form["len"])

    s = Summarizer(text)
    sents = s.summarize(summ_len)
    keywords = s.extract_keywords()
    len1 = len(s.sentences)
    len2 = len(sents)
    return render_template("demo.html", 
                           keywords=keywords,
                           sents=sents, 
                           orig_length=len1,
                           sum_length=len2)


if __name__ == '__main__':
    app.run(debug = True)

