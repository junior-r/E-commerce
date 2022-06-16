class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            self.session['cart'] = {}
            self.cart = self.session['cart']
        else:
            self.cart = cart

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def add(self, producto):
        id = str(producto.id)

        if id not in self.cart.keys():
            # Si el producto no está en el carrito, se agrega con una cantidad = 1
            self.cart[id] = {
                'producto_id': producto.id,
                'imagen': producto.imagen.url,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'description': producto.descripcion,
                'cantidad_vender': 1,
                'monto_total': float(producto.precio)
            }
        else:
            ''' 
                Si el producto ya está en el carrito, se aumenta su cantidad en 1 y el monto total multiplicado 
                por la cantidad
            '''
            self.cart[id]['cantidad_vender'] += 1
            self.cart[id]['monto_total'] = float(self.cart[id]['precio']) * self.cart[id]['cantidad_vender']
        self.save()

    def delete(self, producto):
        id = str(producto.id)
        if id in self.cart:
            del self.cart[id]
            self.save()

    def sub(self, producto):
        id = str(producto.id)
        if id in self.cart.keys():
            self.cart[id]['cantidad_vender'] -= int(1)
            self.cart[id]['monto_total'] -= float(producto.precio)
            if self.cart[id]['cantidad_vender'] <= 0:
                self.delete(producto)
        self.save()

    def clean(self):
        self.session['cart'] = {}
        self.session.modified = True
