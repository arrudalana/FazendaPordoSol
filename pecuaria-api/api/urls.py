from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.realizar_login, name='realizar_login'),
    
    # Proprietários
    path('proprietarios/', views.gerenciar_proprietarios, name='gerenciar_proprietarios'),
    path('proprietarios/<int:id_dono>/', views.detalhe_proprietario, name='detalhe_proprietario'),
    
    # Animais
    path('animais/', views.gerenciar_animais, name='gerenciar_animais'),
    path('animais/<int:id_animal>/', views.detalhe_animal, name='detalhe_animal'),
    
    # Categorias
    path('categorias/', views.gerenciar_categorias, name='gerenciar_categorias'),
    path('categorias/<int:id_categoria>/', views.detalhe_categoria, name='detalhe_categoria'),

    # Leilões
    path('leiloes/', views.gerenciar_leiloes, name='gerenciar_leiloes'),
    path('leiloes/<int:id_leilao>/', views.detalhe_leilao, name='detalhe_leilao'),
]