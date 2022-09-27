from django.contrib import admin
from .models import Movie,Like,DisLike

# Register your models here.
admin.site.register(Movie)
admin.site.register(Like)
admin.site.register(DisLike)
