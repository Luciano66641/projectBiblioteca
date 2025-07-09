from django.shortcuts import render
from .models import Funcionario, Livro, Cliente, Emprestimo, Reserva
from .forms import LivroForm, FuncionarioForm, ClienteForm, EmprestimoForm, ReservaForm, FiltroRelatorioForm, RenovacaoForm, OcorrenciaForm
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import RestrictedError, Count, Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required



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

ORDENACAO_LIVROS_LOOKUP = {
    'titulo': 'titulo',
    'autor': 'autor',
    'editora': 'editora',
    'ano': 'ano_publicacao',
    'isbn': 'isbn',
    'genero': 'genero',
    'quantidade': 'quantidade_disponivel',
}

@login_required
def index(request):
    return render(request, 'biblioteca/index.html')

@login_required
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
    return render(request, 'biblioteca/lista_funcionarios.html', dados)

@login_required
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
    return render(request, 'biblioteca/lista_funcionarios.html', dados)


# def livros(request):
#     livros = Livro.objects.all()
#     dados = {
#         'livros': livros,
#     }
#     return render(request, 'biblioteca/lista_livros.html', dados)

@login_required
def livros(request):
    query = request.GET.get('busca', '')
    livros = Livro.objects.all()

    if query:
        livros = livros.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query) |
            Q(editora__icontains=query) |
            Q(ano_publicacao__icontains=query) |
            Q(genero__icontains=query) |
            Q(isbn__icontains=query)
        )

    dados = {
        'livros': livros,
        'query': query,
    }
    return render(request, 'biblioteca/lista_livros.html', dados)

@login_required
def ordenar_livros(request, campo):
    campo_ordenacao = ORDENACAO_LIVROS_LOOKUP.get(campo)
    busca = request.GET.get('busca', '')
    livros = Livro.objects.all()

    if busca:
        livros = livros.filter(
            Q(titulo__icontains=busca) |
            Q(autor__icontains=busca) |
            Q(editora__icontains=busca) |
            Q(genero__icontains=busca) |
            Q(isbn__icontains=busca)
        )

    if campo_ordenacao:
        livros = livros.order_by(campo_ordenacao)

    return render(request, 'biblioteca/lista_livros.html', {
        'livros': livros,
        'query': busca
    })

@login_required  
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
    return render(request, 'biblioteca/cadastrar_funcionario.html', dados)

@login_required
def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('livros')
    else:
        form = LivroForm()
    
    dados = {  # sempre define 'dados', fora do if/else
        'form': form,
    }
    return render(request, 'biblioteca/cadastrar_livro.html', dados)

@login_required
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

    return render(request, 'biblioteca/editar_funcionario.html', dados)

@login_required
def editar_livro(request, id):

    try:
        livro = Livro.objects.get(id=id)
    except:
        return redirect('livros')

    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES,instance=livro)
        if form.is_valid():
            form.save()
            return redirect('livros')

    form = LivroForm(instance=livro)

    dados = {
        'form': form,
        'livros': livro,
    }

    return render(request, 'biblioteca/editar_livro.html', dados)

@login_required
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

@login_required
def excluir_funcionario(request, id):
    try:
        funcionario = Funcionario.objects.get(id=id)
        funcionario.ativo = False
        funcionario.save()
        messages.success(request, "Funcionário excluído com sucesso.")
    except Funcionario.DoesNotExist:
        messages.error(request, "Funcionário não encontrado.")

    return redirect('funcionarios')

@login_required
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

@login_required
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
    return render(request, 'biblioteca/lista_funcionarios.html', dados)

@login_required
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
    return render(request, 'biblioteca/lista_funcionarios.html', dados)


# clientes

@login_required
def clientes(request):
    query = request.GET.get('busca', '')
    if query:
        clientes = Cliente.objects.filter(ativo=True, nome__icontains=query)
    else:
        clientes = Cliente.objects.filter(ativo=True)

    return render(request, 'biblioteca/lista_clientes.html', {
        'clientes': clientes,
        'ativos': True,
        'query': query
    })

@login_required
def clientes_inativos(request):
    query = request.GET.get('busca', '')
    if query:
        clientes = Cliente.objects.filter(ativo=False, nome__icontains=query)
    else:
        clientes = Cliente.objects.filter(ativo=False)

    return render(request, 'biblioteca/lista_clientes.html', {
        'clientes': clientes,
        'ativos': False,
        'query': query
    })

@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()
    return render(request, 'biblioteca/cadastrar_cliente.html', {'form': form})

@login_required
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
    return render(request, 'biblioteca/editar_cliente.html', {'form': form, 'cliente': cliente})

@login_required
def excluir_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        cliente.ativo = False
        cliente.save()
        messages.success(request, "Cliente excluído com sucesso.")
    except Cliente.DoesNotExist:
        messages.error(request, "Cliente não encontrado.")
    return redirect('clientes')

@login_required
def ativar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        cliente.ativo = True
        cliente.save()
        messages.success(request, "Cliente reativado com sucesso.")
    except Cliente.DoesNotExist:
        messages.error(request, "Cliente não encontrado.")
    return redirect('clientes_inativos')

@login_required
def ordenar_clientes(request, campo):
    campo_ordenacao = ORDENACAO_CLIENTES_LOOKUP.get(campo)
    busca = request.GET.get('busca', '')
    clientes = Cliente.objects.filter(ativo=True)

    if busca:
        clientes = clientes.filter(nome__icontains=busca)

    clientes = clientes.order_by(campo_ordenacao)

    return render(request, 'biblioteca/lista_clientes.html', {
        'clientes': clientes,
        'ativos': True,
        'query': busca
    })

@login_required
def ordenar_clientes_inativos(request, campo):
    campo_ordenacao = ORDENACAO_CLIENTES_LOOKUP.get(campo)
    busca = request.GET.get('busca', '')
    clientes = Cliente.objects.filter(ativo=False)

    if busca:
        clientes = clientes.filter(nome__icontains=busca)

    clientes = clientes.order_by(campo_ordenacao)

    return render(request, 'biblioteca/lista_clientes.html', {
        'clientes': clientes,
        'ativos': False,
        'query': busca
    })

@login_required
def visualizar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    return render(request, 'biblioteca/visualizar_funcionario.html', {
        'funcionario': funcionario
    })

def visualizar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, 'biblioteca/visualizar_cliente.html', {
        'cliente': cliente
    })

@login_required    
def realizar_emprestimo(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)

            if emprestimo.cliente.bloqueado:
                form.add_error('cliente', 'Este cliente está bloqueado e não pode realizar empréstimos.')
            elif emprestimo.livro.quantidade_disponivel > 0:
                emprestimo.livro.quantidade_disponivel -= 1
                emprestimo.livro.save()
                emprestimo.save()
                messages.success(request, "Empréstimo registrado com sucesso!")
                return redirect('livros')
            else:
                form.add_error('livro', 'Livro indisponível no momento.')
    else:
        form = EmprestimoForm()
    return render(request, 'biblioteca/realizar_emprestimo.html', {'form': form})

@login_required
def registrar_devolucao(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id, devolvido=False)

    emprestimo.devolvido = True
    emprestimo.livro.quantidade_disponivel += 1
    emprestimo.livro.save()
    emprestimo.save()

    # Verifica se há reservas pendentes para esse livro
    reserva_pendente = Reserva.objects.filter(livro=emprestimo.livro, notificado=False).order_by('data_reserva').first()
    if reserva_pendente:
        reserva_pendente.notificado = True
        reserva_pendente.save()
        messages.success(request, f"Devolução registrada. Aviso: {reserva_pendente.cliente.nome} foi notificado sobre a reserva do livro '{emprestimo.livro.titulo}'.")
    else:
        messages.success(request, "Devolução registrada com sucesso.")

    return redirect('lista_emprestimos')

@login_required
def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.filter(devolvido=False)
    return render(request, 'biblioteca/lista_emprestimos.html', {'emprestimos': emprestimos})

@login_required
def reservar_livro(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        form.fields['livro'].queryset = Livro.objects.filter(quantidade_disponivel=0)
        if form.is_valid():
            reserva = form.save(commit=False)

            if reserva.cliente.bloqueado:
                form.add_error('cliente', 'Este cliente está bloqueado e não pode reservar livros.')
            elif reserva.livro.quantidade_disponivel == 0:
                reserva.save()
                messages.success(request, "Reserva registrada com sucesso.")
                return redirect('livros')
            else:
                form.add_error('livro', 'Este livro está disponível. Utilize o menu de empréstimo.')
    else:
        form = ReservaForm()
        form.fields['livro'].queryset = Livro.objects.filter(quantidade_disponivel=0)
    return render(request, 'biblioteca/reservar_livro.html', {'form': form})

@login_required
def gerar_relatorio(request):
    relatorio = []
    form = FiltroRelatorioForm()

    if request.method == 'POST':
        form = FiltroRelatorioForm(request.POST)
        if form.is_valid():
            data_inicio = form.cleaned_data['data_inicio']
            data_fim = form.cleaned_data['data_fim']
            tipo = form.cleaned_data['tipo']

            if tipo == 'livros':
                relatorio = (
                    Emprestimo.objects.filter(data_retirada__range=(data_inicio, data_fim))
                    .values('livro__titulo')
                    .annotate(total=Count('id'))
                    .order_by('-total')
                )
            elif tipo == 'usuarios':
                relatorio = (
                    Emprestimo.objects.filter(data_retirada__range=(data_inicio, data_fim))
                    .values('cliente__nome')
                    .annotate(total=Count('id'))
                    .order_by('-total')
                )

    return render(request, 'biblioteca/relatorio.html', {
        'form': form,
        'relatorio': relatorio
    })
    

@login_required   
def renovar_emprestimo(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id, devolvido=False)
    reservas = Reserva.objects.filter(livro=emprestimo.livro, notificado=False).exclude(cliente=emprestimo.cliente)

    if reservas.exists():
        messages.error(request, "Este livro está reservado para outro cliente e não pode ser renovado.")
        return redirect('lista_emprestimos')

    if request.method == 'POST':
        form = RenovacaoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()
            messages.success(request, "Prazo de devolução renovado com sucesso.")
            return redirect('lista_emprestimos')
    else:
        form = RenovacaoForm(instance=emprestimo)

    return render(request, 'biblioteca/renovar_emprestimo.html', {'form': form, 'emprestimo': emprestimo})

@login_required
def registrar_ocorrencia(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id, devolvido=False)

    if request.method == 'POST':
        form = OcorrenciaForm(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()

            # Bloqueia o cliente se marcar como perdido ou danificado
            if emprestimo.status_ocorrencia in ['perdido', 'danificado']:
                emprestimo.cliente.bloqueado = True
                emprestimo.cliente.save()
                messages.warning(request, f"O cliente {emprestimo.cliente.nome} foi bloqueado devido à ocorrência registrada.")

            else:
                messages.success(request, "Ocorrência registrada com sucesso.")

            return redirect('lista_emprestimos')
    else:
        form = OcorrenciaForm(instance=emprestimo)

    return render(request, 'biblioteca/registrar_ocorrencia.html', {'form': form, 'emprestimo': emprestimo})

@login_required
def desbloquear_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.bloqueado = False
    cliente.save()
    messages.success(request, f"Cliente {cliente.nome} foi desbloqueado.")
    return redirect('clientes')

@login_required
def listar_reservas(request):
    reservas = Reserva.objects.all().order_by('-data_reserva')
    return render(request, 'biblioteca/lista_reservas.html', {'reservas': reservas})
    
@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.delete()
    messages.success(request, "Reserva cancelada com sucesso.")
    return redirect('listar_reservas')


