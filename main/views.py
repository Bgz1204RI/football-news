from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from main.forms import NewsForm
from main.models import News
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def show_main(request):
    news_list = News.objects.all()
    context = {
        'npm': '2406453423',
        'name': 'Bagas Zharif Prasetyo',
        'class': 'PBP KI',
        'news_list': news_list,
    }
    return render(request, "main.html", context)

def create_news(request):
    form = NewsForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')
    return render(request, "create_news.html", {'form': form})

def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()
    return render(request, "news_detail.html", {'news': news})

def show_json(request):
    news_list = News.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml(request):
    news_list = News.objects.all()
    xml_data = serializers.serialize("xml", news_list)
    return HttpResponse(xml_data, content_type="application/xml")

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    return render(request, "news_detail.html", {'form': form})


def show_xml_by_id(request, news_id):
    # filter() never raises DoesNotExist; check emptiness instead
    qs = News.objects.filter(pk=news_id)
    if not qs.exists():
        return HttpResponse(status=404)
    xml_data = serializers.serialize("xml", qs)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json_by_id(request, news_id):
    try:
        obj = News.objects.get(pk=news_id)  # get() raises DoesNotExist for 404
    except News.DoesNotExist:
        return HttpResponse(status=404)
    json_data = serializers.serialize("json", [obj])  # wrap single obj in a list
    return HttpResponse(json_data, content_type="application/json")