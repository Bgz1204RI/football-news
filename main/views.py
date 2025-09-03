from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2406453423',
        'name': 'Bagas Zharif Prasetyo',
        'class': 'PBP KI'
    }

    return render(request, "main.html", context)