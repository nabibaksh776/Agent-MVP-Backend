# Generated by Django 5.1.4 on 2024-12-06 19:35

import django.db.models.deletion
import django.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=django.db.models.fields.UUIDField, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chatbot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('website_url', models.URLField(max_length=255)),
                ('date_scrap_time', models.DateTimeField(auto_now_add=True)),
                ('business_information', models.TextField()),
                ('sales_techniques', models.JSONField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('archived', 'Archived')], default='active', max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatbots', to='agentmvp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_content', models.TextField(max_length=500)),
                ('role', models.CharField(choices=[('visitor', 'Visitor'), ('agent', 'Agent')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chatbot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='agentmvp.chatbot')),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='agentmvp.visitor')),
            ],
        ),
        migrations.AddIndex(
            model_name='chatbot',
            index=models.Index(fields=['customer'], name='agentmvp_ch_custome_a1fad1_idx'),
        ),
        migrations.AddIndex(
            model_name='chatbot',
            index=models.Index(fields=['website_url'], name='agentmvp_ch_website_1c1c9e_idx'),
        ),
    ]
