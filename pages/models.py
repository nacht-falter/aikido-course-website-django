from django.db import models
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField


class Category(models.Model):
    """Represents a category to be used for displaying pages on the website"""

    title = models.CharField(_("title"), max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    menu_position = models.IntegerField(_("menu position"), default=0)

    class Meta:
        # https://djangoandy.com/2021/09/01/adjusting-the-plural-of-a-
        # model-in-django-admin/
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["menu_position"]

    def __str__(self):
        return self.title


class Page(models.Model):
    """Represents a page to be displayed on the website"""

    STATUS = ((0, "Draft"), (1, "Published"))

    title = models.CharField(
        _("title"),
        max_length=200,
        unique=True,
        help_text=_("The title of the page")
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text=_("The URL of the page")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_("category"),
        related_name="pages",
        help_text=_("The category of the page (determines the menu position)")
    )
    status = models.IntegerField(
        _("status"),
        choices=STATUS,
        default=0,
        help_text=_("The status of the page (published or draft)")
    )
    featured_image = ThumbnailerImageField(
        _("featured image"),
        upload_to="images/",
        help_text=_("The featured image of the page"),
        blank=True,
        default="placeholder"
    )
    content = models.TextField(_("content"), help_text=_("The page content"))
    menu_position = models.IntegerField(
        _("menu position"),
        default=0,
        help_text=_("The position in the menu (lower numbers appear first)")
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering=["menu_position"]

        verbose_name=_("page")
        verbose_name_plural=_("pages")

    def get_thumbnail_url(self):
        if self.featured_image:
            return self.featured_image['thumbnail'].url
        return None
