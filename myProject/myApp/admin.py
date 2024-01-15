from django.contrib import admin
from myApp.models import *


class Custom_User_Display(admin.ModelAdmin):

    list_display=['display_name','email','user_type']


admin.site.register(Custom_User,Custom_User_Display)
admin.site.register(toLet_model)
admin.site.register(profileProfile)
admin.site.register(rentApplyModel)