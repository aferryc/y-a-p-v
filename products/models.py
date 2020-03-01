from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField(max_length=300)
    price = models.CharField(max_length=100)
    image_list = models.TextField()
    main_image = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def image_arr(self):
        return self.image_list[1:-1].replace("'", "").split(", ")

    @property
    def descriptions(self):
        description = self.description.replace("[", "").replace("]", "")
        if "\r\n" in description:
            return description.split("\r\n")
        elif "\n" in description:
            return description.split("\n")
        else:
            return description


# Create your models here.
