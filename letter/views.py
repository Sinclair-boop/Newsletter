from django.contrib import messages
from django.shortcuts import render, redirect
from . forms import SubscribersFrom, MailMessageForm
from .models import Subscribers
from django.core.mail import  send_mail
from django_pandas.io import read_frame

# Create your views here.
def index(request):

    if request.method == 'POST':
        form = SubscribersFrom(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Suscription Successfull')
            return redirect('/')
    else:
        form = SubscribersFrom()
    context = {
        'form': form,
    }
    return render(request, 'letter/index.html', context)


def mail_letter(request):
    emails = Subscribers.objects.all()
    df = read_frame(emails, fieldnames=['email'])
    mail_list = df['email'].values.tolist()
    print(mail_list)
    if request.method == 'POST':
        form = MailMessageForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('ti tle')
            message = form.cleaned_data.get('message')
            send_mail(
                title,
                message,
                '',
                mail_list,
                fail_silently=False,
            )
            messages.success(request, 'Message has been send to the Mail list')
            return redirect('mail-letter')
    else:
        form = MailMessageForm()
    context = {
        'form': form,
    }

    return render(request, 'letter/mail_letter.html', context)