import os, io
import errno
import urllib
import urllib.request
from time import sleep
import pandas as pd
from urllib.request import urlopen, Request
from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
from googlesearch import search 
from cdqa.utils.converters import pdf_converter
from cdqa.utils.filters import filter_paragraphs
from cdqa.utils.download import download_model, download_bnpp_data
from cdqa.pipeline.cdqa_sklearn import QAPipeline


def search_view(request):
    if request.POST:
        question = request.POST.get('question')
        for idx, url in enumerate(search(question, tld="com", num=10, stop=3, pause=2)): 
            crawl_result(url, idx) 
        # change path to pdfs folder
        df = pdf_converter(directory_path='/path/to/pdfs')
        cdqa_pipeline = QAPipeline(reader='models/bert_qa.joblib')
        cdqa_pipeline.fit_retriever(df)
        prediction = cdqa_pipeline.predict(question)
        data = {
        'answer': prediction[0]
        }
        return JsonResponse(data)
    return render(request, 'search.html')
   

def crawl_result(url, idx):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        bs = BeautifulSoup(html, 'html.parser')
        # change path to pdfs folder
        filename = "/path/to/pdfs/" + str(idx) + ".pdf"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(filename, 'w') as f:
            for line in bs.find_all('p')[:5]:
                f.write(line.text + '\n')
    except (urllib.error.HTTPError, AttributeError) as e:
        pass


