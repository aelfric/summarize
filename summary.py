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
    return "\n".join(s.summarize(text))

@app.route('/demo', methods=['POST'])
def demo():
    text = request.form["text"]
    s = Summarizer()
    sents = s.summarize(text)
    return render_template("demo.html", sents=sents)


if __name__ == '__main__':
    app.run(debug = True)

