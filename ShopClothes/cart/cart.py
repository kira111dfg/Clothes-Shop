from decimal import Decimal
from django.conf import settings
from main.models import Product


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False, size=None):
        product_id = str(product.id)
        key = f"{product_id}:{size}" if size else product_id

        if key not in self.cart:
            self.cart[key] = {'quantity': 0,
                              'price': str(product.price),
                              'size': size}
        if update_quantity:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product, size=None):
        product_id = str(product.id)
        key = f"{product_id}:{size}" if size else product_id

        if key in self.cart:
            del self.cart[key]
            self.save()

    def __iter__(self):
        product_keys = self.cart.keys()
        product_ids = set(key.split(':')[0] for key in product_keys)

        products = Product.objects.filter(id__in=product_ids)
        products_dict = {str(product.id): product for product in products}

        for key, item in self.cart.items():
            product_id, size = key.split(':') if ':' in key else (key, None)
            product = products_dict.get(product_id)
            item['product'] = product
            item['size'] = size
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
