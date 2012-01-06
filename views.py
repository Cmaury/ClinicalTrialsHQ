from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from trials_site.trials.models import *
from trials_site.forms import EmailForm

def home(request):
    return render_to_response('home.html')

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        form = EmailForm(initial={'email':'Enter your email address','condition':q})
        results = []
        condition = Conditions.objects.filter(keyword__icontains=q)
        for i in range(len(condition)):
            key = condition[i].trial_set.all()
            for j in range(len(key)):
                results.append(key[j])
        return render_to_response('search_results.html',
            {'results': results, 'query': q, 'form': form})

def email(request):
    alerts = {}
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            condition = Notification.objects.filter(condition=form['condition'])
            filter = Email.objects.filter(email=form['email'])
            if len(filter) > 0:
                alerts['email_exists']=True
                return render_to_response('search_results.html', {'alerts': alerts, 'email':form['email'], 'condition':form['condition']})
            else:
                if len(condition) > 0:
                    Email.objects.create(email=form['email'])
                    email_id = [Email.objects.order_by('-id')[0].id]
                    condition = condition[0]
                    condition.email = email_id
                    condition.save()
                else:
                    Email.objects.create(email=form['email'])
                    email_id = [Email.objects.order_by('-id')[0].id]
                    n = Notification(condition= form['condition'])
                    n.email = email_id
                    n.save()
                return HttpResponseRedirect('search_result.html')
    else:
        alerts['submitted']= True
        return render_to_response('search_results.html',
        {'alerts': alerts})

def unsubscribe(request, email):
    try:
        emails = Email.objects.get(email=email)
        emails.delete()
        return render_to_response('unsubscribe.html', {'email': email})
    except:
        raise Http404()

def trial(request):
    trial_id = request.path[-11:]
    if trial_id[0:2] != 'NCT':
        results = Trial.objects.get(trial_id=trial_id)
        return render_to_response('trial.html',
            {'result': results})
    else:
        return render_to_response('home.html', {'error': True})
