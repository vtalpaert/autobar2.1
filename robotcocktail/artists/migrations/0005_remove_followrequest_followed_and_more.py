# Generated by Django 4.0.8 on 2023-02-01 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artists', '0004_profile_following_followrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followrequest',
            name='followed',
        ),
        migrations.RemoveField(
            model_name='followrequest',
            name='follower',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='following',
        ),
        migrations.AddField(
            model_name='followrequest',
            name='from_profile',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='follow_requests_sent', to='artists.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='followrequest',
            name='message',
            field=models.TextField(blank=True, help_text='Message', max_length=200),
        ),
        migrations.AddField(
            model_name='followrequest',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Created'), (1, 'Accepted'), (2, 'Rejected')], default=0),
        ),
        migrations.AddField(
            model_name='followrequest',
            name='to_profile',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='follow_requests_received', to='artists.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='followrequest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='follow_requests',
            field=models.ManyToManyField(through='artists.FollowRequest', to='artists.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
