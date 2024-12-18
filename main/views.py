from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from goods.models import Categories, Products
from django.db.models import F, ExpressionWrapper, DecimalField


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем вычисление цены со скидкой для всех продуктов
        products = Products.objects.annotate(
            discounted_price=ExpressionWrapper(
                F('price') * (1 - F('discount') / 100),
                output_field=DecimalField(max_digits=7, decimal_places=2)
            )
        )

        # Передаем все продукты и популярные книги (с рейтингом >= 4)
        context['products'] = products
        context['popular_books'] = products.filter(rating__gte=4).order_by('-rating')[:5]

        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - О нас'
        context['content'] = "О нас"
        context['text_on_page'] = "Текст о том почему этот магазин такой классный, и какой хороший товар."
        return context
    
