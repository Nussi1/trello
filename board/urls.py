from django.urls import path
from . import views


urlpatterns = [

    path("window", views.WindowView.as_view(), name='window'),
    path("window/<int:pk>", views.WindowDetailView.as_view(), name='detail-view'),
    path("window/favourites", views.favourite_list, name='favourite_list'),
    path("window/favourite_add/", views.Windows, name='favourite_adding'),
    path("window/favourite_add/<int:id>/", views.favourite_add, name='favourite_add'),

    path("window/archived", views.archived_list, name='archived_list'),
    path("window/add_to_archive/", views.Archives, name='archived_adding'),
    path("window/add_to_archive/<int:id>/", views.add_to_archive, name='add_to_archive'),

    path("board/<int:pk>", views.EntryDetailView.as_view(), name="entry-detail"),
    path("create", views.EntryCreateView.as_view(), name="entry-create"),
    path("board/<int:pk>/update", views.EntryUpdateView.as_view(), name="entry-list",),
    path("board/<int:pk>/delete", views.EntryDeleteView.as_view(), name="entry-delete",),
    path("board/<int:pk>/", views.CardDetailView.as_view(), name="view_detail"),

    # path("board/", views.ColumnIndexView.as_view(), name='column-list'),
    # path("board/<int:pk>", views.ColumnDetailView.as_view(), name='detail_view'),
    path("board/create", views.ColumnCreateView.as_view(), name='column-create'),
    path("board/<int:pk>/column_update", views.ColumnUpdateView.as_view(), name="column-list", ),
    path("board/<int:pk>/column_delete", views.ColumnDeleteView.as_view(), name="column-delete", ),


    ]