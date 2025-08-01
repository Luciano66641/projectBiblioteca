# Generated by Django 5.2 on 2025-06-12 02:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0005_livro_remove_funcionario_curso_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='genero',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], max_length=3),
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('telefone', models.CharField(max_length=15)),
                ('endereco', models.CharField(max_length=200)),
                ('ativo', models.BooleanField(default=True)),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='clientes', to='academico.livro')),
            ],
        ),
    ]
