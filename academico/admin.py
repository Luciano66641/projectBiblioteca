from django.contrib import admin
from .models import Livro, Funcionario, Cliente

# Register your models here.

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'editora', 'ano_publicacao', 'genero', 'quantidade_disponivel')
    search_fields = ('titulo', 'autor', 'isbn')
    list_filter = ('genero', 'editora', 'ano_publicacao')

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'livro')
    search_fields = ('nome', 'cpf')
    list_filter = ('livro',)