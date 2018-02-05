from django.http import JsonResponse


def index(request):
    return JsonResponse({'name': 'employee manager application',
                         'version': '1.0',
                         'author': 'mateus yano',
                         'endpoints': [
                             '/',
                             '/employee/',
                             '/employee/create/',
                             '/employee/<email>/update/',
                             '/employee/<email>/delete/'
                         ],
                         'contact': 'yano.mateus@gmail.com'})
