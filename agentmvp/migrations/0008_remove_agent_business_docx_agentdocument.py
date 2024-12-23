# Generated by Django 5.1.4 on 2024-12-18 13:09

import agentmvp.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agentmvp', '0007_customer_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='business_docx',
        ),
        migrations.CreateModel(
            name='AgentDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='business_docs/', validators=[agentmvp.models.validate_file_extension])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='agentmvp.agent')),
            ],
        ),
    ]
