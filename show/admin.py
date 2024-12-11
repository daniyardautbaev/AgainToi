from django.contrib import admin
from .models import Host, Photographer, CameraOperator, Dancer, Singer, ShowProfile, ShowOrderAcceptance


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name',)


@admin.register(Photographer)
class PhotographerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name',)


@admin.register(CameraOperator)
class CameraOperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name',)


@admin.register(Dancer)
class DancerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name',)


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name',)


@admin.register(ShowProfile)
class ShowProfileAdmin(admin.ModelAdmin):
    list_display = ('show_name', 'user', 'host', 'get_dancers', 'get_singers')
    search_fields = ('show_name',)
    list_filter = ('host',)
    filter_horizontal = ('dancer', 'singer')

    def get_dancers(self, obj):
        return ", ".join([d.name for d in obj.dancer.all()])
    get_dancers.short_description = 'Dancers'

    def get_singers(self, obj):
        return ", ".join([s.name for s in obj.singer.all()])
    get_singers.short_description = 'Singers'


@admin.register(ShowOrderAcceptance)
class ShowOrderAcceptanceAdmin(admin.ModelAdmin):
    list_display = ('order', 'show', 'accepted', 'accepted_date')
    search_fields = ('order__user__username', 'show__show_name')
