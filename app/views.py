import imp
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'app/home.html')


def contacto(request):
    if request.method == 'POST':
        dir_email = request.POST['dir_email'] # Email que el usuario ingrese en el input.
        asunto = request.POST['asunto'] # Asunto del email.
        subject = request.POST['subject'] + ' Att: ' + dir_email # Mensaje del usuario.

        template = render_to_string('app/email_template.html', {'dir_name': dir_email, 'subject': subject})

        email = EmailMessage(
            asunto,
            template,
            settings.EMAIL_HOST_USER,
            ['junior31064049@gmail.com']
        )

        email.fail_silently = False
        email.send()

        messages.success(request, 'Tu Correo ha sido enviado con exito!.')
        return render(request, 'app/contacto.html')
    return render(request, 'app/contacto.html')


def productos(request):
    return render(request, 'app/productos.html')
