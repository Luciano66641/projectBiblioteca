from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField


GENERO_CHOICES_HUMAN = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro'),
]

ESTADO_CIVIL_CHOICES = [
    ('S', 'Solteiro'),
    ('C', 'Casado'),
    ('D', 'Divorciado'),
    ('V', 'Viúvo'),
]

ESCOLARIDADE_CHOICES = [
    ('fun', 'Fundamental'),
    ('med', 'Médio'),
    ('sup', 'Superior'),
    ('pos', 'Pós-graduação'),
    ('mes', 'Mestrado'),
    ('dou', 'Doutorado'),
]

GENERO_CHOICES = [
    ('romance', 'Romance'),
    ('ficcao', 'Ficção'),
    ('nao_ficcao', 'Não Ficção'),
    ('biografia', 'Biografia'),
    ('poesia', 'Poesia'),
    ('aventura', 'Aventura'),
    ('drama', 'Drama'),
    ('outro', 'Outro'),
]

STATUS_OCORRENCIA = [
    ('normal', 'Normal'),
    ('perdido', 'Perdido'),
    ('danificado', 'Danificado'),
]

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    editora = models.CharField(max_length=100)
    ano_publicacao = models.PositiveIntegerField()
    isbn = models.CharField(max_length=20, unique=True)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
    quantidade_disponivel = models.PositiveIntegerField(default=1)
    foto = StdImageField(
        upload_to='fotos/alunos',
        variations={'thumb': (150, 150), 'medium': (300, 300)},
        blank=True,
        null=True
    )


    def __str__(self):
        return f"{self.titulo} ({self.ano_publicacao})"

    def save(self, *args, **kwargs):
        self.titulo = self.formatar_titulo(self.titulo)
        self.autor = self.formatar_nome(self.autor)
        self.editora = self.editora.title()
        super().save(*args, **kwargs)

    def formatar_titulo(self, titulo):
        minusculas = ['da', 'de', 'do', 'das', 'dos', 'e', 'em', 'a', 'o']
        partes = titulo.lower().split()
        return ' '.join([p if p in minusculas else p.capitalize() for p in partes])

    def formatar_nome(self, nome):
        return ' '.join([parte.capitalize() for parte in nome.split()])


class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    genero = models.CharField(max_length=3, choices=GENERO_CHOICES_HUMAN)
    estado_civil = models.CharField(
        max_length=30, choices=ESTADO_CIVIL_CHOICES)
    escolaridade = models.CharField(
        max_length=50, choices=ESCOLARIDADE_CHOICES)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = self.formatar_nome(self.nome)
        super().save(*args, **kwargs)

    def formatar_nome(self, nome):
        partes = nome.lower().split()
        minusculas = ['da', 'de', 'do', 'das', 'dos', 'e']

        return ' '.join([
            p if p in minusculas else p.capitalize()
            for p in partes
        ])


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=200)
    livro = models.ForeignKey(
        Livro, on_delete=models.RESTRICT, related_name="clientes")
    ativo = models.BooleanField(default=True)
    bloqueado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = self.formatar_nome(self.nome)
        super().save(*args, **kwargs)

    def formatar_nome(self, nome):
        partes = nome.lower().split()
        minusculas = ['da', 'de', 'do', 'das', 'dos', 'e']
        return ' '.join([p if p in minusculas else p.capitalize() for p in partes])
    
class Emprestimo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_retirada = models.DateField(default=timezone.now)
    data_devolucao_prevista = models.DateField()
    devolvido = models.BooleanField(default=False)
    status_ocorrencia = models.CharField(max_length=20, choices=STATUS_OCORRENCIA, default='normal')

    def __str__(self):
        return f"{self.cliente.nome} - {self.livro.titulo}"

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_reserva = models.DateTimeField(default=timezone.now)
    notificado = models.BooleanField(default=False)

    def __str__(self):
        return f"Reserva de {self.livro.titulo} para {self.cliente.nome}"
