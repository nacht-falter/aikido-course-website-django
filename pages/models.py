from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel, models.Model):
    """Represents a category to be used for displaying pages on the website"""

    translations = TranslatedFields(
        title=models.CharField(_("title"), max_length=200),
    )
    slug = models.SlugField(max_length=200, unique=True)
    menu_position = models.IntegerField(_("menu position"), default=0)

    class Meta:
        # https://djangoandy.com/2021/09/01/adjusting-the-plural-of-a-
        # model-in-django-admin/
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["menu_position"]

    def _generate_unique_slug(self):
        from parler.utils.context import switch_language

        # Try to use German title for slug generation, fallback to current language if German doesn't exist
        try:
            with switch_language(self, 'de'):
                slug = slugify(self.title)
        except Exception:
            # If German translation doesn't exist yet, use current language
            slug = slugify(self.title)

        if not slug:
            # If we still don't have a slug, return existing or empty
            return self.slug if self.slug else ''

        if self.slug and self.slug.startswith(slug):
            return self.slug

        unique_slug = slug
        num = 1

        while Category.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
            unique_slug = f'{slug}-{num}'
            num += 1

        return unique_slug

    def save(self, *args, **kwargs):
        # Only generate slug if we have a title
        if hasattr(self, 'title') and self.title:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Page(TranslatableModel, models.Model):
    """Represents a page to be displayed on the website"""

    STATUS = ((0, "Draft"), (1, "Published"))

    translations = TranslatedFields(
        title=models.CharField(
            _("title"),
            max_length=200,
        ),
        content=models.TextField(_("content")),
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_("category"),
        related_name="pages",
    )
    status = models.IntegerField(
        _("status"),
        choices=STATUS,
        default=0,
    )
    featured_image = ThumbnailerImageField(
        _("featured image"),
        upload_to="images/",
        blank=True,
        default="placeholder"
    )
    menu_position = models.IntegerField(
        _("menu position"),
        default=0,
    )

    def _generate_unique_slug(self):
        from parler.utils.context import switch_language

        # Try to use German title for slug generation, fallback to current language if German doesn't exist
        try:
            with switch_language(self, 'de'):
                slug = slugify(self.title)
        except Exception:
            # If German translation doesn't exist yet, use current language
            slug = slugify(self.title)

        if not slug:
            # If we still don't have a slug, return existing or empty
            return self.slug if self.slug else ''

        if self.slug and self.slug.startswith(slug):
            return self.slug

        unique_slug = slug
        num = 1

        while Page.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
            unique_slug = f'{slug}-{num}'
            num += 1

        return unique_slug

    def save(self, *args, **kwargs):
        # Only generate slug if we have a title
        if hasattr(self, 'title') and self.title:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

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
