from django.contrib import admin
from .models import Livreto


class AdminLivreto(admin.ModelAdmin):
    pass


admin.site.register(Livreto, AdminLivreto)