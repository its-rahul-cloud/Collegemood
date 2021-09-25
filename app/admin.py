from django.contrib import admin
from .models import (Profile,College,Post)
# Register your models here.
#@admin.register(Profile)
#class ProfileModelAdmin(admin.ModelAdmin):
 #   list_display = ['id','user','college_name','image','location']
admin.site.register(Profile)


@admin.register(College)
class CollegeModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','image','about']

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
   list_display = [ 'id','type','author','date_posted']



