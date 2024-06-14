from django.db import models


class Category(models.Model):
    """Represents a category to be used for displaying pages on the website"""

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    menu_position = models.IntegerField(default=0)

    class Meta:
        # https://djangoandy.com/2021/09/01/adjusting-the-plural-of-a-
        # model-in-django-admin/
        verbose_name_plural = "categories"
        ordering = ["menu_position"]

    def __str__(self):
        return self.title


class Page(models.Model):
    """Represents a page to be displayed on the website"""

    STATUS = ((0, "Draft"), (1, "Published"))

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="pages"
    )
    status = models.IntegerField(choices=STATUS, default=0)
    featured_image = models.ImageField(upload_to="images/")
    content = models.TextField()
    menu_position = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["menu_position"]
