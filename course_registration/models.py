from django.db import models

REGISTRATION_STATUS = ((0, "Closed"), (1, "Open"))


class Course(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    registration_status = models.IntegerField(
        choices=REGISTRATION_STATUS, default=0
    )
    course_fee = models.IntegerField()

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.title
