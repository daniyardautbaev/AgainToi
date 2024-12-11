from django.contrib import admin

from main.models import SearchHistory, EventType


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'search_query', 'search_date')
    search_fields = ('user',)


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image')
    search_fields = ('name',)
