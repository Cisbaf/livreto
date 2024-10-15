from django.urls import path
from livreto import views


urlpatterns = [
    path('', views.livreto_index, name='livreto_index'),
    path('infos/<str:system>', views.livreto_infos, name='livreto_infos'),
    path('render/<str:slug>', views.livreto_render, name='livreto_render'),
    path('pdf/<str:slug>', views.livreto_render_pdf, name='livreto_pdf'),
    path('page/<str:slug>/<int:num>', views.livreto_render_page_as_image, name='livreto_render_page'),
    path('page/<str:slug>/<int:num>/<int:dpi>', views.livreto_render_page_as_image, name='livreto_render_page_dpi'),
    path('register', views.livreto_register, name='livreto_register'),
    path('update/<int:pk>', views.livreto_update, name='livreto_update'),
    path('delete/<int:pk>', views.livreto_delete, name='livreto_delete'),
]