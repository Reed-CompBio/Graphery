from django.contrib import admin
from .models import model_list


for model in model_list:
    admin.site.register(model)
