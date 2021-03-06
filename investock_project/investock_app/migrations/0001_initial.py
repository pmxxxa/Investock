# Generated by Django 3.2.3 on 2021-05-28 18:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255, unique=True)),
                ('company_symbol', models.CharField(blank=True, default='', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='YahooStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regular_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('change', models.DecimalField(decimal_places=10, max_digits=20)),
                ('change_percentages', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(-100.0), django.core.validators.MaxValueValidator(100.0)])),
                ('download_date', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investock_app.company')),
            ],
        ),
        migrations.CreateModel(
            name='UserForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecast_date', models.DateField()),
                ('forecast_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('excess_or_shortage', models.CharField(max_length=255, null=True)),
                ('difference', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('real_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investock_app.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('edited', models.BooleanField(default=False)),
                ('edition_time', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('yahoo_stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investock_app.yahoostock')),
            ],
        ),
    ]
