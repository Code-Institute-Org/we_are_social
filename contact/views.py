from django.shortcuts import render
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = EmailMessage()
            email.from_email = form.cleaned_data.get('email')
            email.to = ['brian@codeinstitute.net']
            email.topic = form.cleaned_data.get('topic')
            email.body = form.cleaned_data.get('message')
            our_form = form.save(commit=False)
            our_form.save()
            email.send()
            messages.add_message(request, messages.SUCCESS, 'Your contact message has been sent. Thank you.')
            return render(request, 'index.html')
        else:
            render(request, 'contact.html')

    else:
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})
