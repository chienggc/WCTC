from django.contrib import admin

# Register your models here.
from .models import PointLog
from members.models import Award
from .models import Product
from .models import Category
from .models import Redemption

admin.site.register(Award)
admin.site.register(Category)
admin.site.register(PointLog)
admin.site.register(Product)
admin.site.register(Redemption)
