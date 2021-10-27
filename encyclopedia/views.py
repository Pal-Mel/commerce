from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random
from django import forms

from . import util

class NewArticleForms( forms.Form) :
    article = forms.CharField(label="Найменування статті",widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label= "", widget=forms.Textarea(attrs={'class': 'form-control', 'style' :"height:100%; margin:5px 0px;"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def article(request, name):
    content = util.get_entry(name)
    if (content == None):
        return render(request, "encyclopedia/article.html", {
            "name": f'Стаття з назвою {name} не знайдена',
            "content": ""
        })
    md = markdown2.Markdown()
    result = md.convert(content)
    return render(request, "encyclopedia/article.html", {
        "name": name,
        "content": result
    })


def search(request):
    enc_list = []
    if request.method == "POST":
        form = request.POST
        wiki_list = util.list_entries()
        wiki_list_lower = []
        for wiki in wiki_list:
            wiki_list_lower.append(wiki.lower())
        if form['q'].lower() in wiki_list_lower:
            return HttpResponseRedirect(f"/enc/wiki/{form['q']}")
        else:
            for wiki in wiki_list:
                if wiki.lower().find(form['q']) != -1:
                    enc_list.append(wiki)
            return render(request, "encyclopedia/search.html", {
                "entries": enc_list
                })

def add(request):
    if request.method == "POST":
        form = NewArticleForms(request.POST)
        if form.is_valid() :
            article = form.cleaned_data["article"]
            content = form.cleaned_data["content"]
            old_content=util.get_entry(article)
            if old_content==None:
                util.save_entry(article, content)
                return HttpResponseRedirect(f"/wiki/{article}")
            else:
                return render(request, "./encyclopedia/add.html", {
                        "form": form,
                        "error": f"Стаття з назвою '{article}' вже існує. Змініть назву."
                        })
        else:
            return render(request, "./encyclopedia/add.html", {
            "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewArticleForms()
            })

def edit(request, name):
    content = util.get_entry(name)
    return render(request, "encyclopedia/edit.html", {
            "form": NewArticleForms({'article':name,'content':content}),
            "title_page":name
                })


def saveedit(request):
    if request.method == "POST":
        form = NewArticleForms(request.POST)
        if form.is_valid() :
            article = form.cleaned_data["article"]
            content = form.cleaned_data["content"]
            util.save_entry(article, content)
            return HttpResponseRedirect(f"/enc/wiki/{article}")

def randompage(request):
    pages =  util.list_entries()
    rand = random.choice(pages)
    return HttpResponseRedirect(f"/enc/wiki/{rand}")