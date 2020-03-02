from django.apps import AppConfig

class ProductsConfig(AppConfig):
    name = "products"

    def ready(self):
        from products.models import Product
        from products.jobs import crawl_data
        for product in Product.objects.all():
            crawl_data(product.url, repeat=3600)
        pass
