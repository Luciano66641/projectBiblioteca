from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('alunos/', views.alunos, name='alunos'),
    path('cursos/', views.cursos, name='cursos'),
    path('cadastrar_aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('cadastrar_curso/', views.cadastrar_curso, name='cadastrar_curso'),
    path('editar_aluno/<int:id>/', views.editar_aluno, name='editar_aluno'),
    path('editar_curso/<int:id>/', views.editar_curso, name='editar_curso'),
    path('excluir_curso/<int:id>/', views.excluir_curso, name='excluir_curso'),
    path('excluir_aluno/<int:id>/', views.excluir_aluno, name='excluir_aluno'),
    path('alunos/inativos/', views.alunos_inativos, name='alunos_inativos'),
    path('alunos/ativar/<int:id>/', views.ativar_aluno, name='ativar_aluno'),
]
