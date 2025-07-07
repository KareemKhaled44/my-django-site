from django.contrib import admin
from userauths.models import User, Contact
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'created_at', 'email', 'subject', 'status')


admin.site.register(User, UserAdmin)
admin.site.register(Contact, ContactAdmin)