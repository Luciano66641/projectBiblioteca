from .models import Cliente
from django import forms
from .models import Livro, Funcionario

# Formulário para Livro


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro  # Aqui vamos dizer que o formulário vai usar o modelo Livro
        # Aqui vamos dizer quais campos do modelo Livro queremos usar no formulário
        fields = '__all__'


# Formulário para Funcionários
class FuncionarioForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Funcionario  # Aqui vamos dizer qual modelo esse formulário vai usar
        fields = ['nome', 'data_nascimento', 'cpf', 'genero',
                  'estado_civil', 'escolaridade']
        # Aqui vamos dizer quais campos do modelo funcionario queremos usar no formulário


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'telefone', 'endereco', 'livro']
