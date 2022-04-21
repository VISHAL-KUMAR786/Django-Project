# this is created by human
from hashlib import new
from os import remove
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    text = {"name": "vishal"}
    return render(request, 'index.html', text)


def analyze(request):

    indexText = request.POST.get('text', '')

    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    numberemover = request.POST.get('numberemover', 'off')

    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    if removepunc == "on":
        newTxt = ""
        for char in indexText:
            if char not in punctuations:
                newTxt += char
        indexText = newTxt

    if removepunc == "on":
        newTxt = indexText
        newTxt = newTxt.upper()
        indexText = newTxt

    if newlineremover == "on":
        newTxt = ""
        for char in indexText:
            if char == "\n" or char == "\r":
                newTxt += " "
            else:
                newTxt += char
        indexText = newTxt

    if extraspaceremover == "on":
        newTxt = " ".join(indexText.split())
        # there is strip function also
        indexText = newTxt

    if numberemover == "on":
        newTxt = " ".join(indexText.split())
        no = [0,1,2,3,4,5,6,7,8,9]
        str1 = ""
        for i in newTxt:
            if i.isnumeric() :
                pass 
            else:
                str1  = str1 + i
        indexText = str1

    if(removepunc != "on" and fullcaps != "on" and newlineremover != "on" and extraspaceremover != "on"):
        return HttpResponse("some error")

    return render(request, 'analyze.html', {"name": "vishal", "text": indexText})


def message(request):
    return render(request, 'message.html', {"name": "vishal"})
