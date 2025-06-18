from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from .models import CatalogueItem, Category, OrderModel  # Certifica-te que OrderModel está importado


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        cosplay = CatalogueItem.objects.filter(category__name__contains='Cosplay')
        fidget = CatalogueItem.objects.filter(category__name__contains='Fidget')
        custom_parts = CatalogueItem.objects.filter(category__name__contains='Custom Part')
        toys = CatalogueItem.objects.filter(category__name__contains='Toy')

        context = {
            'cosplay': cosplay,
            'fidget': fidget,
            'custom_parts': custom_parts,
            'toys': toys,
        }

        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        district = request.POST.get('district')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')  # Receber os itens do form

        for item in items:
            catalogue_item = CatalogueItem.objects.get(pk=int(item))
            item_data = {
                'id': catalogue_item.pk,
                'name': catalogue_item.name,
                'price': catalogue_item.price
            }
            order_items['items'].append(item_data)

        # Calcular preço total e IDs
        price = sum(item['price'] for item in order_items['items'])
        item_ids = [item['id'] for item in order_items['items']]

        # Criar encomenda
        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            district=district,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        #A seguir de tudo estar feito, envia confrimação por EMAIL
        
        body = ('Thank you for your order! Blaze is preparing your 3D Prints! :)\n'
            f'Your total: {price}\n')
        
        send_mail(
            subject='Thank you for your purchase!',
            message='Blaze team will prepare your order. Hope you like your new 3D Prints!',
            from_email='noreply@blazeshop.com',
            recipient_list=['cliente@exemplo.com'],
            fail_silently=False,
        )

        # Contexto para a página de confirmação
        context = {
            'items': order_items['items'],
            'price': price
        }
        return redirect('order-confirmation', pk=order.pk)
    
class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items.all(),
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        print(request.body)

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


