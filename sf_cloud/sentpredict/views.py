from django.shortcuts import render
from django.http import JsonResponse



# Create your views here.

def predict(request):
    return JsonResponse({'data': [{
        'content': "hoom nafsdf fsdf",
        'classification': 'neutral'
    }, {
        'content': "hoom nafsdf fsdf",
        'classification': 'positive'
    }, {
        'content': "hoom nafsdf fsdsdff",
        'classification': 'positive'
    }, {
        'content': "hoom nafsdf fsdsdff",
        'classification': 'negative'
    }]})
