from django.shortcuts import render


def v404_view(request, exception=None, template_name='404.html'):
    return render(request, '404.html')