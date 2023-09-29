from django.shortcuts import render, redirect
from django.http import HttpResponse
from random import choice
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def content(request, title):
    entry_content = util.get_entry(title)
    if entry_content:
        return render(request, "encyclopedia/content.html", {
            "content_title": title,
            "content": markdown2.markdown(entry_content)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error_content": "404 - Not Found"
        })


def search(request):
    query = request.GET.get('q', None)

    if not query:
        return redirect('/')
    elif util.get_entry(query):
        return redirect(f"wiki/{query}")
    else:
        entries = util.list_entries()
        matchs = []

        for entry in entries:
            if query.lower() in entry.lower():
                matchs.append(entry)
        return render(request, "encyclopedia/search.html", {
            'matchs': matchs,
            'query': query
        })


def new(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "error_content": "This entry already exists"
            })

        text = request.POST.get('text')

        with open(f"entries/{title}.md", "w") as new_file:
            new_file.write(text)

        return redirect(f"/wiki/{title}")

    return render(request, "encyclopedia/new.html")


def edit(request, title):
    if request.method == 'POST':
        text = request.POST.get('text')

        with open(f"entries/{title}.md", 'w') as file:
            file.write(text)

        return redirect(f"/wiki/{title}")


    return render(request, "encyclopedia/edit.html", {
        'content': util.get_entry(title),
        'title': title
    })


def random_page(_):
    return redirect(f"/wiki/{choice(util.list_entries())}")


