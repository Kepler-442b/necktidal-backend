# Generated by Django 3.0.3 on 2020-03-16 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('institution', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'discount_information',
            },
        ),
        migrations.CreateModel(
            name='DiscountPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=300, null=True)),
                ('discount_rate', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
            options={
                'db_table': 'discount_plans',
            },
        ),
        migrations.CreateModel(
            name='FavoriteAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'favorite_albums',
            },
        ),
        migrations.CreateModel(
            name='FavoriteArtist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'favorite_artists',
            },
        ),
        migrations.CreateModel(
            name='FavoriteTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'favorite_tracks',
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'genders',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
                ('is_email', models.BooleanField(default=False)),
                ('is_push', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'notifications',
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'playlists',
            },
        ),
        migrations.CreateModel(
            name='PlaylistTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'playlist_tracks',
            },
        ),
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_email', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'social_accounts',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_hifi', models.BooleanField(default=False)),
                ('base_price', models.DecimalField(decimal_places=2, default=9.99, max_digits=10)),
            ],
            options={
                'db_table': 'subscriptions',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=256)),
                ('social_email', models.EmailField(max_length=256, null=True)),
                ('password', models.CharField(max_length=100)),
                ('thumbnail_url', models.URLField(max_length=2000, null=True)),
                ('birthday', models.DateField(null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('language', models.CharField(max_length=50, null=True)),
                ('is_subscribed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Notification')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.User')),
            ],
        ),
    ]
