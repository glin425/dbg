from django.contrib import admin

# Register your models here.
from app.models import UsersGroup, Users, Clients, Hosting, Domains, ClientsUsers


class UsersGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('name', )
    list_filter = ('name',)

admin.site.register(UsersGroup, UsersGroupAdmin)

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'mobile', 'avatar')
    search_fields = ('user',)
    ordering = ('user', )
    list_filter = ('user',)

admin.site.register(Users, UsersAdmin)

class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name',)
    ordering = ('name', )
    list_filter = ('name',)

admin.site.register(Clients, ClientsAdmin)

class ClientsUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'user')
    search_fields = ('client', 'user')
    ordering = ('client', 'user')
    list_filter = ('client', 'user')

admin.site.register(ClientsUsers, ClientsUsersAdmin)

class DomainsAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'name', 'expiration_date', 'year_price', 'month_price')
    search_fields = ('client', 'name', 'expiration_date', 'year_price', 'month_price')
    ordering = ('-expiration_date', )
    list_filter = ('name',)

admin.site.register(Domains, DomainsAdmin)

class HostingAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'domain', 'name', 'expiration_date', 'year_price', 'month_price')
    search_fields = ('client', 'name', 'domain', 'expiration_date', 'year_price', 'month_price')
    ordering = ('-expiration_date', )
    list_filter = ('name',)

admin.site.register(Hosting, HostingAdmin)