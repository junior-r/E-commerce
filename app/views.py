from datetime import datetime
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.contrib import messages
from .models import Producto, Coupon
from django.core.paginator import Paginator
from django.http import Http404
from .forms import CustomUserCreationForm, CouponForm
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
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
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

    for p in productos:
        if p.cantidad <= 0:
            cart = Cart(request)
            cart.delete(producto=p)
            p.delete()
            return redirect('productos')
        else:
            pass

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
        'asunto': asunto,
        'username': request.user.username,
        'user_id': request.user.id
    }
    products_cart = []
    subtotal = 0
    IVA = 0.16  # 16%

    for k, v in request.session['cart'].items():
        products_cart.append(v)
        subtotal += float(v['monto_total'])

    data['total'] = subtotal * IVA + subtotal
    data['subtotal'] = subtotal
    data['products_cart'] = products_cart
    code = request.session['coupon']

    if code: # Si el usuario tiene un cupon.
        try:
            coupon = Coupon.objects.get(code=code)
        except:
            messages.error(request, 'Cupón no válido')
            return redirect('cart')
        if coupon.active:
            data['coupon'] = coupon
            data['total_cart_coupon'] = subtotal - (subtotal * float(coupon.discount) / 100)
            data['total'] = data['total_cart_coupon'] * IVA + data['total_cart_coupon']
            messages.success(request, 'Cupón aplicado correctamente!')
            request.session['coupon'] = None
        else:
            messages.error(request, 'Cupón no activo!')

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
def generate_coupon(request):
    coupons = Coupon.objects.all()

    data = {
        'form': CouponForm(),
        'coupons': coupons
    }

    letters_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letters_lower = letters_upper.lower()
    numbers = '0123456789'
    code = ''
    for i in range(0, 8):
        code += random.choice(letters_upper + letters_lower + numbers)

    if request.method == 'POST' and request.user.is_superuser:
        form = CouponForm(request.POST)
        if form.is_valid():
            discount = form.cleaned_data.get('discount')
            valid_from = form.cleaned_data.get('valid_from')
            valid_to = form.cleaned_data.get('valid_to')
            active = form.cleaned_data.get('active')

            coupon = Coupon(code=code, discount=discount, valid_from=valid_from, valid_to=valid_to, active=active)
            coupon.save()
            messages.success(request, 'Cupón creado correctamente!')
            return redirect(to='generate_coupon')
        else:
            data['form'] = form
            messages.error(request, 'Ocurrió un error, ¡vuelva a intentar!')

    return render(request, 'app/coupons.html', data)


@login_required
def cart(request):
    global producto
    data = {
        'cart': request.session['cart']
    }

    productos = []
    subtotal = 0
    IVA = 0.16  # 16%
    cart = request.session['cart']
    count = 0

    for k, v in cart.items():
        producto = Producto.objects.get(id=int(k))
        productos.append(producto)
        count += 1

        subtotal += float(v['monto_total'])

    data['total'] = subtotal * IVA + subtotal
    data['number_prd_cart'] = count
    data['productos'] = productos
    data['total_cart'] = subtotal

    if request.method == 'GET':
        code = request.GET.get('coupon')

        if code:
            try:
                coupon = Coupon.objects.get(code=code)
                request.session['coupon'] = code
            except:
                messages.error(request, 'Cupón no válido')
                return redirect('cart')
            if coupon.active:
                data['coupon'] = coupon
                data['total_cart_coupon'] = subtotal - (subtotal * float(coupon.discount) / 100)
                data['total'] = data['total_cart_coupon'] * IVA + data['total_cart_coupon']
                messages.success(request, 'Cupón aplicado correctamente!')
            else:
                messages.error(request, 'Cupón no activo!')

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


@login_required
def clean_cart(request):
    cart = Cart(request)
    cart.clean()
    return redirect('cart')
