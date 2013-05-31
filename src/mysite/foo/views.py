# Create your views here.
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from foo.models import Book
import datetime

def index(request):
    return render_to_response('foo/index.html', None)

def display_meta(request):
    values = request.META.items()
    values.sort()
    return render_to_response('foo/display_meta.html', {'meta_data': values})

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('foo/current_datetime.html', {'current_date': now})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def search(request):
    errors = None
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors = 'Enter a search term.'
        elif len(q) > 20:
            errors = 'Please enter at most 20 characters.'
        else:
            books = Book.objects.filter(title__icontains=q)
            return render(request, 'foo/search_results.html',
                {'books': books, 'query': q})
    return render(request, 'foo/search_form.html',
        {'errors': errors})
    
def contact(request):
    if request.method == 'GET':
        return render(request, 'foo/contact_form.html')
    
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
#            send_mail(
#                request.POST['subject'],
#                request.POST['message'],
#                request.POST.get('email', 'noreply@example.com'),
#                ['siteowner@example.com'],
#            )
            return HttpResponseRedirect('thanks/')
    return render(request, 'foo/contact_form.html',
        {'errors': errors})

def contact_thanks(request):
    if request.method == 'GET':
        return HttpResponse("Thanks")