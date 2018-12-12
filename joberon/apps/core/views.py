from django.shortcuts import render, redirect, reverse, HttpResponse


def letsencrypt1(request):
    return HttpResponse(
        'NYvG5kyM6uxSJDwFzgGqCC03WF9y721xqSxCH8g4eYg.Rcz4GO0RowCnc8vJIFndcvLvBAeyxtvb4YW18BFeaPY',
        content_type='text/plain'
    )


def letsencrypt2(request):
    return HttpResponse(
        'o1ibN3hYY07uUOiLjZicbeTI7_x9w6vIXj3LN7Uawaw.Rcz4GO0RowCnc8vJIFndcvLvBAeyxtvb4YW18BFeaPY',
        content_type='text/plain'
    )


def index(request):
    return render(request, 'index.html')

