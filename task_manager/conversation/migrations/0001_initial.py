# Generated by Django 4.2 on 2023-04-27 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_alter_task_created_by_alter_task_task_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recieved_conversation', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Sent_conversation', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to='core.task')),
            ],
        ),
    ]
