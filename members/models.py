from django.db import models


# Create your models here.
class Award(models.Model):
    award_name = models.CharField('Award Name', max_length=50, unique=True)
    award_point = models.IntegerField()
    color_code = models.CharField('Award Color Code', max_length=10, unique=True, null=True)

    def __str__(self):
        return self.award_name + " - " + str(self.award_point)
