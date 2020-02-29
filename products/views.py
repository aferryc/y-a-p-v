from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, TemplateView
from products.models import Product
from products.jobs import crawl_data


class List(ListView):
    model = Product
    paginate_by = 10
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Detail(DetailView):
    model = Product
    fields = ["name", "description", "price", "image_list"]
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Add(TemplateView):
    model = Product
    template_name = "add_product.html"

    def post(self, request):
        product_url = request.POST["product_url"]
        print(product_url)
        crawl_data.now(product_url)
        crawl_data(product_url, repeat=3600)
        return HttpResponseRedirect("/products")
