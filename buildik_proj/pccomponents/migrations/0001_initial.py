# Generated by Django 3.1.4 on 2020-12-15 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormFactor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formfactor_name', models.CharField(default=None, max_length=30, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interface_name', models.CharField(default=None, max_length=30, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(default=None, max_length=30)),
                ('model', models.CharField(default=None, max_length=30)),
                ('category', models.IntegerField(choices=[(1, 'CPU'), (2, 'Motherboard'), (3, 'GPU'), (4, 'RAM'), (5, 'Storage'), (6, 'Power supply unit'), (7, 'CPU Cooler'), (8, 'Case')], default=None)),
                ('price', models.FloatField()),
            ],
            options={
                'unique_together': {('manufacturer', 'model')},
            },
        ),
        migrations.CreateModel(
            name='MemoryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memorytype_name', models.CharField(default=None, max_length=30, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Socket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('socket_name', models.CharField(default=None, max_length=30, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pccomponents.item')),
                ('max_cooler_length', models.IntegerField()),
                ('max_gpu_length', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('pccomponents.item',),
        ),
        migrations.CreateModel(
            name='CPUCooler',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pccomponents.item')),
                ('radiator_size', models.IntegerField()),
                ('cooler_length', models.IntegerField()),
                ('fan_rpm', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('pccomponents.item',),
        ),
        migrations.CreateModel(
            name='GPU',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pccomponents.item')),
                ('memory', models.IntegerField()),
                ('core_clock', models.IntegerField()),
                ('TDP', models.IntegerField(null=True)),
                ('gpu_length', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('pccomponents.item',),
        ),
        migrations.CreateModel(
            name='Motherboard',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pccomponents.item')),
                ('max_memory', models.IntegerField()),
                ('memory_slots', models.IntegerField()),
                ('max_ram_clock', models.IntegerField()),
                ('formfactor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pccomponents.formfactor')),
                ('memorytype', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pccomponents.memorytype')),
                ('socket', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pccomponents.socket')),
            ],
            options={
                'abstract': False,
            },
            bases=('pccomponents.item',),
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pccomponents.item')),
                ('capacity', models.IntegerField()),
                ('cache', models.IntegerField()),
                ('interface', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pccomponents.interface')),
            ],
            options={
                'abstract': False,
            },
            bases=('pccomponents.item',),
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pccomponents.item')),
                ('memory', models.IntegerField()),
                ('memory_clock', models.IntegerField()),
                ('memorytype', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pccomponents.memorytype')),
            ],
            options={
                'abstract': False,
            },
            bases=('pccomponents.item',),
        ),
        migrations.CreateModel(
            name='PowerSupplyUnit',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pccomponents.item')),
                ('wattage', models.IntegerField()),
                ('efficiency_rating', models.CharField(default=None, max_length=30, null=True)),
                ('formfactor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pccomponents.formfactor')),
            ],
            options={
                'abstract': False,
            },
            bases=('pccomponents.item',),
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pccomponents.item')),
                ('core_clock', models.FloatField()),
                ('cores', models.IntegerField()),
                ('L3_cache', models.IntegerField()),
                ('max_ram_clock', models.IntegerField()),
                ('max_memory', models.IntegerField()),
                ('TDP', models.IntegerField(null=True)),
                ('process', models.IntegerField(null=True)),
                ('integrated_graphics', models.CharField(default=None, max_length=30, null=True)),
                ('socket', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pccomponents.socket')),
            ],
            options={
                'abstract': False,
            },
            bases=('pccomponents.item',),
        ),
        migrations.CreateModel(
            name='MotherboardInterface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('interface', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pccomponents.interface')),
                ('motherboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pccomponents.motherboard')),
            ],
            options={
                'unique_together': {('motherboard', 'interface')},
            },
        ),
        migrations.CreateModel(
            name='CPUCoolerSocket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('socket', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pccomponents.socket')),
                ('cpucooler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pccomponents.cpucooler')),
            ],
            options={
                'unique_together': {('cpucooler', 'socket')},
            },
        ),
        migrations.CreateModel(
            name='CaseFormFactor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formfactor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pccomponents.formfactor')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pccomponents.case')),
            ],
            options={
                'unique_together': {('case', 'formfactor')},
            },
        ),
    ]
