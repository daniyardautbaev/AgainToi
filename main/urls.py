from django.urls import path
from .views import SearchPlacesView, SearchShowsView, EventTypeListView, venue_profile_user, profile_user, \
    show_profile_user

urlpatterns = [
    path('search/places/', SearchPlacesView.as_view(), name='search_places'),
    path('search/shows/', SearchShowsView.as_view(), name='search_shows'),
    path('event-types/', EventTypeListView.as_view(), name='event_types'),
    path('venue/<int:pk>/', venue_profile_user, name='venue_profile_user'),
    path('show/<int:pk>/', show_profile_user, name='show_profile_user'),
    path('user/<int:pk>/', profile_user, name='profile_user'),
]
