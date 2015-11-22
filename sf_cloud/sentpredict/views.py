from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from . import utility
import pickle
import chardet

# Create your views here.

def predict(request):
    if request.method == 'POST':
        paragraph = None
        try:
            paragraph = request.POST['content'].encode('utf-8')
        except Exception as e:
            return HttpResponseForbidden("Error: %s" % e.message)

        if paragraph is None or len(paragraph) < 1:
            return HttpResponseForbidden("Please enter paragraph content")

        dist = pickle.load(open('ref_data/0228.dat', 'r'))
        classifier = utility.ClassifySentence(dist)
        data = classifier.predict_sentences(paragraph)

        return JsonResponse({
            'data': data
        })
    else:
        return HttpResponseForbidden()
        # classifier = utility.ClassifySentence()
