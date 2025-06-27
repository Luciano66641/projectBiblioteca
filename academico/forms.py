from django import forms
from django.core.validators import RegexValidator
from .models import Livro, Funcionario, Cliente, Emprestimo, Reserva

# Validador: apenas números
somente_numeros = RegexValidator(r'^\d+$', 'Este campo deve conter apenas números.')

TIPO_RELATORIO = [
    ('livros', 'Livros mais emprestados'),
    ('usuarios', 'Usuários com mais empréstimos'),
]

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'editora': forms.TextInput(attrs={'class': 'form-control'}),
            'ano_publicacao': forms.NumberInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'quantidade_disponivel': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class FuncionarioForm(forms.ModelForm):
    cpf = forms.CharField(validators=[somente_numeros])
    telefone = forms.CharField(validators=[somente_numeros])
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Funcionario
        fields = ['nome', 'data_nascimento', 'cpf', 'telefone', 'genero', 'estado_civil', 'escolaridade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'escolaridade': forms.Select(attrs={'class': 'form-control'}),
        }

class ClienteForm(forms.ModelForm):
    cpf = forms.CharField(validators=[somente_numeros])
    telefone = forms.CharField(validators=[somente_numeros])

    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'telefone', 'endereco', 'livro']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'livro': forms.Select(attrs={'class': 'form-control'}),
        }

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['cliente', 'livro', 'data_retirada', 'data_devolucao_prevista']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'livro': forms.Select(attrs={'class': 'form-control'}),
            'data_retirada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_devolucao_prevista': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'livro']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'livro': forms.Select(attrs={'class': 'form-control'}),
        }


class FiltroRelatorioForm(forms.Form):
    data_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    data_fim = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    tipo = forms.ChoiceField(choices=TIPO_RELATORIO, widget=forms.Select(attrs={'class': 'form-control'}))
    
    
class RenovacaoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['data_devolucao_prevista']
        widgets = {
            'data_devolucao_prevista': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['status_ocorrencia']
        widgets = {
            'status_ocorrencia': forms.Select(attrs={'class': 'form-control'})
        }
