from django.contrib import admin
from .models import *


admin.site.register(Category)

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('stage','user','timestamp')
    
admin.site.register(Applicant,ApplicantAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display = ('title','is_published','is_closed','timestamp')

admin.site.register(Stage,JobAdmin)

class BookmarkJobAdmin(admin.ModelAdmin):
    list_display = ('stage','user','timestamp')
admin.site.register(BookmarkJob,BookmarkJobAdmin)


