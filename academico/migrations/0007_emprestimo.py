# Generated by Django 5.2 on 2025-06-26 23:02

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0006_alter_funcionario_genero_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_retirada', models.DateField(default=django.utils.timezone.now)),
                ('data_devolucao_prevista', models.DateField()),
                ('devolvido', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.cliente')),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.livro')),
            ],
        ),
    ]
