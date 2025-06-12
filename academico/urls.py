from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('funcionarios/', views.funcionario, name='funcionarios'),
    path('livros/', views.livros, name='livros'),
    path('cadastrar_funcionario/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'),
    path('editar_funcionario/<int:id>/', views.editar_funcionario, name='editar_funcionario'),
    path('editar_livro/<int:id>/', views.editar_livro, name='editar_livro'),
    path('excluir_livro/<int:id>/', views.excluir_livro, name='excluir_livro'),
    path('excluir_funcionario/<int:id>/', views.excluir_funcionario, name='excluir_funcionario'),
    path('funcionarios/inativos/', views.funcionarios_inativos, name='funcionarios_inativos'),
    path('funcionarios/ativar/<int:id>/', views.ativar_funcionario, name='ativar_funcionario'),
    path('funcionarios/ordenar/<campo>/', views.ordenar_funcionarios, name='ordenar_funcionarios'), 
    path('funcionarios/ordenar/inativos/<campo>/', views.ordenar_funcionarios_inativos, name='ordenar_funcionarios_inativos'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/inativos/', views.clientes_inativos, name='clientes_inativos'),
    path('clientes/cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
    path('clientes/ativar/<int:id>/', views.ativar_cliente, name='ativar_cliente'),
    path('clientes/ordenar/<campo>/', views.ordenar_clientes, name='ordenar_clientes'),
    path('clientes/ordenar/inativos/<campo>/', views.ordenar_clientes_inativos, name='ordenar_clientes_inativos'),
]
