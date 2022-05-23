from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.contrib import messages
from .models import Producto
from django.core.paginator import Paginator
from django.http import Http404
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .Cart import Cart

# Create your views here.


def home(request):
    count = 0
    data = {}
    if 'cart' in request.session.keys():
        cart = request.session['cart']

        for k, v in cart.items():
            count += 1

        data['number_prd_cart'] = count
        data['cart'] = cart
    return render(request, 'app/home.html', data)


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

    if 'cart' in request.session.keys():
        count = 0
        cart = request.session['cart']

        for k, v in cart.items():
            count += 1

        data['number_prd_cart'] = count
        data['cart'] = cart

    return render(request, 'app/productos.html', data)


def view_producto(request, nombre, id):
    producto = Producto.objects.get(id=id, nombre=nombre)
    data = {
        'producto': producto,
        'producto_id': str(producto.id)
    }

    if request.user.is_authenticated and 'cart' in request.session.keys():
        count = 0
        cart = request.session['cart']
        data['cart'] = cart.keys()

        for k, v in cart.items():
            count += 1
        data['number_prd_cart'] = count
    return render(request, 'app/view_producto.html', data)


@login_required
def send_pedido_cart(request, email_user, asunto):
    data = {
        'email_user': email_user,
        'asunto': asunto
    }
    products_cart = []
    total_cart = 0

    for k, v in request.session['cart'].items():
        products_cart.append(v)
        total_cart += float(v['monto_total'])

    data['total_cart'] = total_cart
    data['products_cart'] = products_cart

    template = get_template('app/pedido_email.html')
    content = template.render(data)

    email = EmailMultiAlternatives(
        'Correo de Pedidos',
        asunto,
        settings.EMAIL_HOST_USER,  # From email
        [settings.EMAIL_HOST_USER]  # To email
    )

    email.attach_alternative(content, 'text/html')
    try:
        email.send()
        messages.success(request, 'Pedido enviado con éxito, Pronto responderemos!')
    except:
        messages.error(request, 'Ocurrió un error, ¡vuelva a intentar!')


@login_required
def cart(request):
    data = {
        'cart': request.session['cart']
    }

    if request.user.is_authenticated and 'cart' in request.session.keys():
        productos = []
        total_cart = 0
        cart = request.session['cart']
        count = 0

        for k, v in cart.items():
            producto = Producto.objects.get(id=int(k))
            productos.append(producto)
            count += 1

            total_cart += float(v['monto_total'])

        data['number_prd_cart'] = count
        data['productos'] = productos
        data['total_cart'] = total_cart

    if request.method == 'POST':
        email_user = request.POST.get('email_user')
        asunto = request.POST.get('asunto')
        send_pedido_cart(request, email_user, asunto)
        return redirect('cart')

    return render(request, 'app/cart.html', data)


@login_required
def add_prd_cart(request, id, nombre):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=id)
    cart.add(producto)

    return redirect('view_producto', nombre=producto.nombre,  id=producto.id)


@login_required
def incr_prd_cart(request, id, nombre):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=id)
    cart.add(producto)

    return redirect('cart')


@login_required
def sub_prd_cart(request, id, nombre):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=id)
    cart.sub(producto)

    return redirect('cart')


@login_required
def del_prd_cart(request, id, nombre):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=id)
    cart.delete(producto)

    return redirect('view_producto', nombre=producto.nombre,  id=producto.id)
