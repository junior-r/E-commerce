from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from .models import Producto
from django.core.paginator import Paginator
from django.http import Http404
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    
    return render(request, 'app/home.html')


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    data = {
        'user': user
    }
    return render(request, 'app/profile.html', data)


def registro(request):
    data = {
        'form': CustomUserCreationForm
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()

            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            login(request, user)
            messages.success(request, 'Cuenta creada correctamente!')

            return redirect(to='home')
        data['form'] = formulario

    return render(request, 'registration/registro.html', data)


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
        try:
            email.send()
            messages.success(request, 'Tu Correo ha sido enviado con exito!.')
        except:
            messages.error(request, 'Ha ocurrido un error al enviar el Email')
    return render(request, 'app/contacto.html')


def productos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(productos, 16)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator
    }
    return render(request, 'app/productos.html', data)
