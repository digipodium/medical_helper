from django.contrib import admin
from .models import Contact, Order, Profile,Equipment,EquipmentRental,Human_Resource,Purchase,ServiceRequest,Report

# Register your models here.
admin.site.register(Equipment)
admin.site.register(EquipmentRental)
admin.site.register(Human_Resource)
admin.site.register(Purchase)
admin.site.register(Report)
admin.site.register(Contact)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''

    list_display = ('buyer','product','status','date')
    ordering = ('date','status',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Admin View for Profile'''

    list_display = ('Full_Name','user','address','email','mobile','update_on')
    ordering = ('update_on','user')
    search_fields = ('Full_Name','address')


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    '''Admin View for ServiceRequest'''

    list_display = ('hr','for_user','durations','gender','age','request_for','service_is_complete')
    
    