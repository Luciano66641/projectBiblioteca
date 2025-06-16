from django.shortcuts import render
from .models import Funcionario, Livro, Cliente
from .forms import LivroForm, FuncionarioForm, ClienteForm
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import RestrictedError
from django.shortcuts import get_object_or_404

ORDENACAO_FUNCIONARIOS_LOOKUP = {
    'nome': 'nome',
    'genero': 'genero',
    'escolaridade': 'escolaridade',
    'estado_civil': 'estado_civil',
    'data_nascimento': 'data_nascimento'
}

ORDENACAO_CLIENTES_LOOKUP = {
    'nome': 'nome',
    'cpf': 'cpf',
    'telefone': 'telefone',
    'endereco': 'endereco',
    'livro': 'livro__titulo'
}

# Create your views here.


def index(request):
    return render(request, 'academico/index.html')


def funcionario(request):
    query = request.GET.get('busca', '')
    if query:
        funcionarios = Funcionario.objects.filter(
            ativo=True, nome__icontains=query)
    else:
        funcionarios = Funcionario.objects.filter(ativo=True)
    dados = {
        'funcionarios': funcionarios,
        'ativos': True,
        'query': query,
    }
    return render(request, 'academico/lista_funcionarios.html', dados)


def funcionarios_inativos(request):
    query = request.GET.get('busca', '')
    if query:
        funcionarios = Funcionario.objects.filter(
            ativo=False, nome__icontains=query)
    else:
        funcionarios = Funcionario.objects.filter(ativo=False)

    dados = {
        'funcionarios': funcionarios,
        'ativos': False,
        'query': query
    }
    return render(request, 'academico/lista_funcionarios.html', dados)


def livros(request):
    livros = Livro.objects.all()
    dados = {
        'livros': livros,
    }
    return render(request, 'academico/lista_livros.html', dados)


def cadastrar_funcionario(request):

    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('funcionarios')
    else:
        form = FuncionarioForm()
        dados = {
            'form': form,
        }
    return render(request, 'academico/cadastrar_funcionario.html', dados)


def cadastrar_livro(request):

    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('livros')
    else:
        form = LivroForm()
        dados = {
            'form': form,
        }
    return render(request, 'academico/cadastrar_livro.html', dados)


def editar_funcionario(request, id):

    try:
        funcionario = Funcionario.objects.get(id=id)
    except:
        return redirect('funcionarios')

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('funcionarios')

    # form vai receber um formulário com os dados do funcionario selecionado.
    form = FuncionarioForm(instance=funcionario)

    # Montamos o dicionário com os dados para ser passado para o template.
    dados = {
        'form': form,
        'funcionario': funcionario,
    }

    return render(request, 'academico/editar_funcionario.html', dados)


def editar_livro(request, id):

    try:
        livro = Livro.objects.get(id=id)
    except:
        return redirect('livros')

    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            return redirect('livros')

    form = LivroForm(instance=livro)

    dados = {
        'form': form,
        'livros': livro,
    }

    return render(request, 'academico/editar_livro.html', dados)


def excluir_livro(request, id):
    try:
        livro = Livro.objects.get(id=id)
        livro.delete()
        messages.success(request, "Livro excluído com sucesso.")
    except RestrictedError:
        messages.error(
            request, "Não é possível deletar o livro pois há Clientes vinculados.")
    except Livro.DoesNotExist:
        messages.error(request, "livro não encontrado.")

    return redirect('livros')


def excluir_funcionario(request, id):
    try:
        funcionario = Funcionario.objects.get(id=id)
        funcionario.ativo = False
        funcionario.save()
        messages.success(request, "Funcionário excluído com sucesso.")
    except Funcionario.DoesNotExist:
        messages.error(request, "Funcionário não encontrado.")

    return redirect('funcionarios')


def ativar_funcionario(request, id):
    try:
        funcionario = Funcionario.objects.get(id=id)
    except Funcionario.DoesNotExist:
        messages.error(request, "Funcionário não encontrado.")
        return redirect('funcionarios_inativos')

    if funcionario.ativo == False:
        funcionario.ativo = True
        funcionario.save()
        messages.success(request, "Funcionário reativado com sucesso.")

    else:
        messages.info(request, "O funcionário já está ativo.")

    return redirect('funcionarios_inativos')


def ordenar_funcionarios(request, campo):
    campo_ordenacao = ORDENACAO_FUNCIONARIOS_LOOKUP.get(campo)
    busca = request.GET.get('busca', '')
    funcionarios = Funcionario.objects.filter(ativo=True)

    if busca:
        funcionarios = funcionarios.filter(nome__icontains=busca)

    funcionarios = funcionarios.order_by(campo_ordenacao)
    dados = {
        'funcionarios': funcionarios,
        'ativos': True,
        'query': busca,
    }
    return render(request, 'academico/lista_funcionarios.html', dados)


def ordenar_funcionarios_inativos(request, campo):
    campo_ordenacao = ORDENACAO_FUNCIONARIOS_LOOKUP.get(campo)
    busca = request.GET.get('busca', '')
    funcionarios = Funcionario.objects.filter(ativo=False)

    if busca:
        funcionarios = Funcionario.objects.filter(nome__icontains=busca)

    funcionarios = funcionarios.order_by(campo_ordenacao)
    dados = {
        'funcionarios': funcionarios,
        'ativos': False,
        'query': busca,
    }
    return render(request, 'academico/lista_funcionarios.html', dados)


# clientes


def clientes(request):
    query = request.GET.get('busca', '')
    if query:
        clientes = Cliente.objects.filter(ativo=True, nome__icontains=query)
    else:
        clientes = Cliente.objects.filter(ativo=True)

    return render(request, 'academico/lista_clientes.html', {
        'clientes': clientes,
        'ativos': True,
        'query': query
    })


def clientes_inativos(request):
    query = request.GET.get('busca', '')
    if query:
        clientes = Cliente.objects.filter(ativo=False, nome__icontains=query)
    else:
        clientes = Cliente.objects.filter(ativo=False)

    return render(request, 'academico/lista_clientes.html', {
        'clientes': clientes,
        'ativos': False,
        'query': query
    })


def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()
    return render(request, 'academico/cadastrar_cliente.html', {'form': form})


def editar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except:
        return redirect('clientes')

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')

    form = ClienteForm(instance=cliente)
    return render(request, 'academico/editar_cliente.html', {'form': form, 'cliente': cliente})


def excluir_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        cliente.ativo = False
        cliente.save()
        messages.success(request, "Cliente excluído com sucesso.")
    except Cliente.DoesNotExist:
        messages.error(request, "Cliente não encontrado.")
    return redirect('clientes')


def ativar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        cliente.ativo = True
        cliente.save()
        messages.success(request, "Cliente reativado com sucesso.")
    except Cliente.DoesNotExist:
        messages.error(request, "Cliente não encontrado.")
    return redirect('clientes_inativos')


def ordenar_clientes(request, campo):
    campo_ordenacao = ORDENACAO_CLIENTES_LOOKUP.get(campo)
    busca = request.GET.get('busca', '')
    clientes = Cliente.objects.filter(ativo=True)

    if busca:
        clientes = clientes.filter(nome__icontains=busca)

    clientes = clientes.order_by(campo_ordenacao)

    return render(request, 'academico/lista_clientes.html', {
        'clientes': clientes,
        'ativos': True,
        'query': busca
    })


def ordenar_clientes_inativos(request, campo):
    campo_ordenacao = ORDENACAO_CLIENTES_LOOKUP.get(campo)
    busca = request.GET.get('busca', '')
    clientes = Cliente.objects.filter(ativo=False)

    if busca:
        clientes = clientes.filter(nome__icontains=busca)

    clientes = clientes.order_by(campo_ordenacao)

    return render(request, 'academico/lista_clientes.html', {
        'clientes': clientes,
        'ativos': False,
        'query': busca
    })

def visualizar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    return render(request, 'academico/visualizar_funcionario.html', {
        'funcionario': funcionario
    })

def visualizar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, 'academico/visualizar_cliente.html', {
        'cliente': cliente
    })