from django import forms
from django.core.validators import RegexValidator
from .models import Livro, Funcionario, Cliente

# Validador: apenas números
somente_numeros = RegexValidator(r'^\d+$', 'Este campo deve conter apenas números.')

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
