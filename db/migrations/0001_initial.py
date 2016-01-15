# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import db.models.user_profile
import db.models.warranty_image
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('buyer_type', models.CharField(max_length=20, choices=[('KIDS', 'Kids'), ('MENS', 'Mens'), ('WOMENS', 'Womens')], default='KIDS')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Name')),
                ('phone', models.CharField(max_length=30, null=True, verbose_name='Phone Number')),
                ('email', models.CharField(max_length=100, null=True, verbose_name='Email')),
                ('not_available', models.BooleanField(default=False, verbose_name='Not Available')),
            ],
            options={
                'verbose_name_plural': 'Buyers',
                'verbose_name': 'Buyer',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DataOption',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('option_type', models.CharField(max_length=20, choices=[('PRE-BOOK', 'Pre-Book Options'), ('WARRANTY_DAMAGE', 'Warranty Damage')], default='PRE-BOOK')),
                ('description', models.CharField(max_length=50, default='', null=True, verbose_name='Description')),
                ('value', models.CharField(max_length=100, null=True, verbose_name='Value')),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort Order')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Data Options',
                'verbose_name': 'Data Option',
                'ordering': ['option_type'],
            },
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('file_type', models.CharField(max_length=20, choices=[('AD', 'Ad'), ('MEDIA_PLAYER', 'Media Player'), ('PRODUCT', 'Product')], default='AD')),
                ('file_path', models.FileField(upload_to='media_file/%Y/%m/%d')),
                ('file_name', models.CharField(max_length=50, null=True, verbose_name='File Name')),
                ('file_extension', models.CharField(max_length=10, null=True, verbose_name='File Extension')),
                ('description', models.CharField(max_length=255, null=True, verbose_name='Description')),
                ('uploaded', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Media Files',
                'verbose_name': 'Media File',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='MediaPlayer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('audience', models.CharField(max_length=30, choices=[('EVERYONE', 'Everyone'), ('DEALER', 'Dealer'), ('REP', 'Rep')], default='ALL')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('enabled', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Media Players',
                'verbose_name': 'Media Player',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='MediaPlayerSlide',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('slide_type', models.CharField(max_length=30, choices=[('IMAGE', 'Image'), ('YOUTUBE', 'YouTube Video'), ('VIMEO', 'Vimeo Video')], default='IMAGE')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('video_code', models.CharField(max_length=50, null=True, verbose_name='Video Code')),
                ('sort_order', models.IntegerField(default=0)),
                ('media_file', models.ForeignKey(null=True, to='db.MediaFile', verbose_name='Media File', related_name='media_player_slides')),
                ('media_player', models.ForeignKey(null=True, to='db.MediaPlayer', verbose_name='Media Player', related_name='media_player_slides')),
            ],
            options={
                'verbose_name_plural': 'Media Player Slides',
                'verbose_name': 'Media Player Slide',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('message_type', models.CharField(max_length=20, choices=[('EVERYONE', 'Everyone'), ('DEALER', 'Dealer'), ('REP', 'Rep')], default='EVERYONE', verbose_name='Message for')),
                ('message_date', models.DateTimeField(verbose_name='Message date', auto_now_add=True)),
                ('title', models.CharField(max_length=30, null=True, verbose_name='Title')),
                ('message', models.TextField(null=True, verbose_name='Message')),
                ('enabled', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Messages',
                'verbose_name': 'Message',
            },
        ),
        migrations.CreateModel(
            name='ModelInventory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('model_sku', models.CharField(max_length=50, null=True, verbose_name='Model Sku')),
                ('model_inventory', models.IntegerField(default=0, verbose_name='Model Inventory')),
                ('inventory_sku', models.CharField(max_length=50, null=True, verbose_name='Inventory Sku')),
                ('inventory', models.IntegerField(default=0, verbose_name='Inventory')),
                ('replacement_sku', models.CharField(max_length=50, null=True, verbose_name='Replacement Sku')),
                ('pending', models.IntegerField(default=0, verbose_name='Pending')),
                ('threshold', models.IntegerField(default=0, verbose_name='Threshold')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Model Inventory',
                'verbose_name': 'Model Inventory',
                'ordering': ['model_sku'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('order_source', models.CharField(max_length=50, default='', null=True, verbose_name='Order Source')),
                ('in_house_sales', models.CharField(max_length=50, default='', null=True, verbose_name='In House Sales')),
                ('po_number', models.CharField(max_length=50, default='', null=True, verbose_name='PO Number')),
                ('status', models.CharField(max_length=20, choices=[('NEW', 'New Order'), ('SUBMIT', 'Submitted'), ('PROCESSING', 'Processing'), ('SHIPPED', 'Shipped')], default='NEW')),
                ('order_type', models.CharField(max_length=20, choices=[('AT-ONCE', 'At Once'), ('PRE-BOOK', 'Pre-Book'), ('PROPOSE', 'Proposed')], default='AT-ONCE')),
                ('status_date', models.DateTimeField(auto_now_add=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('prebook_date', models.DateTimeField(null=True)),
                ('cancel_date', models.DateTimeField(null=True)),
                ('pre_book_option', models.CharField(max_length=100, null=True, verbose_name='Pre-Book Option')),
                ('notes', models.TextField(null=True, verbose_name='Notes')),
                ('billto_name', models.CharField(max_length=100, blank=True, verbose_name='Bill To Name')),
                ('billto_address1', models.CharField(max_length=50, null=True, verbose_name='Bill To Address')),
                ('billto_address2', models.CharField(max_length=50, null=True, verbose_name='Bill To Address')),
                ('billto_city', models.CharField(max_length=50, null=True, verbose_name='Bill To City')),
                ('billto_state', models.CharField(max_length=30, null=True, verbose_name='Bill To State')),
                ('billto_postal_code', models.CharField(max_length=9, null=True, verbose_name='Bill To Zip Code')),
                ('billto_country', models.CharField(max_length=50, null=True, verbose_name='Bill To Country')),
                ('billto_phone', models.CharField(max_length=30, null=True, verbose_name='Bill To Phone Number')),
                ('billto_email', models.CharField(max_length=100, null=True, verbose_name='Bill To Email')),
                ('shipto_name', models.CharField(max_length=100, blank=True, verbose_name='Ship To Name')),
                ('shipto_address_id', models.CharField(max_length=200, null=True, verbose_name='Ship To Address ID')),
                ('shipto_address1', models.CharField(max_length=50, null=True, verbose_name='Ship To Address')),
                ('shipto_address2', models.CharField(max_length=50, null=True, verbose_name='Ship To Address')),
                ('shipto_city', models.CharField(max_length=50, null=True, verbose_name='Ship To City')),
                ('shipto_state', models.CharField(max_length=30, null=True, verbose_name='Ship To State')),
                ('shipto_postal_code', models.CharField(max_length=9, null=True, verbose_name='Ship To Zip Code')),
                ('shipto_country', models.CharField(max_length=50, null=True, verbose_name='Ship To Country')),
                ('shipto_phone', models.CharField(max_length=30, null=True, verbose_name='Ship To Phone Number')),
                ('shipto_email', models.CharField(max_length=100, null=True, verbose_name='Ship To Email')),
            ],
            options={
                'verbose_name_plural': 'Orders',
                'verbose_name': 'Order',
                'ordering': ['order_date'],
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('quantity', models.IntegerField(default=1, null=True, verbose_name='Quantity')),
                ('sku', models.CharField(max_length=50, null=True, verbose_name='Sku')),
                ('item_number', models.CharField(max_length=50, null=True, verbose_name='Item Number')),
                ('style', models.CharField(max_length=50, null=True, verbose_name='Style')),
                ('description', models.CharField(max_length=50, null=True, verbose_name='Description')),
                ('size', models.CharField(max_length=50, null=True, verbose_name='Size')),
                ('upc', models.CharField(max_length=50, null=True, verbose_name='UPC')),
                ('cost', models.DecimalField(max_digits=7, default=0, verbose_name='Cost', decimal_places=2)),
                ('price', models.DecimalField(max_digits=7, default=0, verbose_name='Price', decimal_places=2)),
                ('order', models.ForeignKey(null=True, to='db.Order', verbose_name='Order', related_name='order_details')),
            ],
            options={
                'verbose_name_plural': 'Order Details',
                'verbose_name': 'Order Detail',
                'ordering': ['sku'],
            },
        ),
        migrations.CreateModel(
            name='OrderSource',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('description', models.CharField(max_length=50, default='', help_text='Description displayed on order screen', null=True, verbose_name='Description')),
                ('value', models.CharField(max_length=100, help_text='Value attached to order', null=True, verbose_name='Value')),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort Order')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Order Sources',
                'verbose_name': 'Order Source',
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('item_number', models.CharField(max_length=50, null=True, verbose_name='Item Number')),
                ('description', models.CharField(max_length=50, null=True, verbose_name='Description')),
                ('image_path', models.ImageField(upload_to='product_images', null=True)),
                ('available', models.DateField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Product Items',
                'verbose_name': 'Product Item',
                'ordering': ['item_number'],
            },
        ),
        migrations.CreateModel(
            name='ProductSku',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('sku', models.CharField(max_length=50, null=True, verbose_name='Sku')),
                ('item_number', models.CharField(max_length=50, null=True, verbose_name='Item Number')),
                ('style', models.CharField(max_length=50, null=True, verbose_name='Style')),
                ('description', models.CharField(max_length=50, null=True, verbose_name='Description')),
                ('size', models.CharField(max_length=50, null=True, verbose_name='Size')),
                ('upc', models.CharField(max_length=50, null=True, verbose_name='UPC')),
                ('cost', models.DecimalField(max_digits=7, default=0, verbose_name='Cost', decimal_places=2)),
                ('wholesale', models.DecimalField(max_digits=7, default=0, verbose_name='Wholesale', decimal_places=2)),
                ('msrp', models.DecimalField(max_digits=7, default=0, verbose_name='MSRP', decimal_places=2)),
                ('inventory', models.IntegerField(default=0, verbose_name='Inventory')),
                ('active', models.BooleanField(default=False)),
                ('product_item', models.ForeignKey(null=True, to='db.ProductItem', verbose_name='Product Item', related_name='product_skus')),
            ],
            options={
                'verbose_name_plural': 'Product Skus',
                'verbose_name': 'Product Sku',
                'ordering': ['sku'],
            },
        ),
        migrations.CreateModel(
            name='ProductStyle',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('style_sku', models.CharField(max_length=50, null=True, verbose_name='Style Sku')),
                ('style', models.CharField(max_length=50, null=True, verbose_name='Style')),
            ],
            options={
                'verbose_name_plural': 'Product Styles',
                'verbose_name': 'Product Style',
                'ordering': ['style_sku'],
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('address_type', models.CharField(max_length=20, choices=[('BILLTO', 'Bill To'), ('SHIPTO', 'Ship To')], default='BILLTO')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('address_id', models.CharField(max_length=200, null=True, verbose_name='Address ID')),
                ('address1', models.CharField(max_length=50, null=True, verbose_name='Address')),
                ('address2', models.CharField(max_length=50, null=True, verbose_name='Address')),
                ('city', models.CharField(max_length=50, null=True, verbose_name='City')),
                ('state', models.CharField(max_length=30, null=True, verbose_name='State')),
                ('postal_code', models.CharField(max_length=9, null=True, verbose_name='Postal Code')),
                ('country', models.CharField(max_length=30, null=True, verbose_name='Country')),
            ],
            options={
                'verbose_name_plural': 'User Addresses',
                'verbose_name': 'User Address',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('user_type', models.CharField(max_length=20, choices=[('ADMIN', 'Administrator'), ('CUSTOMER_SERVICE', 'Customer Service'), ('DEALER', 'Dealer'), ('REP', 'Rep')], default='DEALER')),
                ('account_id', models.CharField(max_length=50, null=True, verbose_name='Account Id')),
                ('company', models.CharField(max_length=100, null=True, verbose_name='Company')),
                ('phone', models.CharField(max_length=30, null=True, verbose_name='Phone Number')),
                ('terms', models.CharField(max_length=50, null=True, verbose_name='Terms')),
                ('shipping_method', models.CharField(max_length=50, null=True, verbose_name='Shipping Method')),
                ('discount', models.DecimalField(max_digits=4, default=0, verbose_name='Discount', decimal_places=2)),
                ('notes', models.TextField(null=True, default='')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('locked', models.BooleanField(default=False)),
                ('terms_accepted', models.BooleanField(default=False, verbose_name='Terms Accepted')),
                ('terms_uploaded', models.BooleanField(default=False, verbose_name='Terms Uploaded')),
                ('terms_file_path', models.FileField(blank=True, upload_to=db.models.user_profile.get_terms_upload_to)),
                ('eula_accepted', models.BooleanField(default=False, verbose_name='EULA Accepted')),
                ('warranty_receiver', models.BooleanField(default=False, verbose_name='Warranty Receiver Role')),
                ('warranty_authorizer', models.BooleanField(default=False, verbose_name='Warranty Authorizer Role')),
                ('account_rep', models.ForeignKey(null=True, to='db.UserProfile', related_name='rep')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Profiles',
                'verbose_name': 'User Profile',
            },
        ),
        migrations.CreateModel(
            name='Warranty',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('claim_number', models.CharField(max_length=50, null=True, verbose_name='Claim Number')),
                ('status', models.CharField(max_length=20, choices=[('NEW', 'New Claim'), ('PREAUTHORIZED', 'Pre-Authorized'), ('RECEIVED', 'Received'), ('AUTHORIZED', 'Authorized'), ('NOTAUTHORIZED', 'Not Authorized'), ('CLOSED', 'Closed')], default='NEW')),
                ('status_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Name')),
                ('email', models.CharField(max_length=100, null=True, verbose_name='Email')),
                ('phone', models.CharField(max_length=50, null=True, verbose_name='Phone')),
                ('address', models.CharField(max_length=100, null=True, verbose_name='Address')),
                ('style', models.CharField(max_length=50, null=True, verbose_name='Style')),
                ('color', models.CharField(max_length=50, null=True, verbose_name='Color')),
                ('damage', models.CharField(max_length=100, null=True, verbose_name='Damage')),
                ('image_override', models.BooleanField(default=False, verbose_name='Image Override')),
                ('email_sent', models.BooleanField(default=False, verbose_name='Email Sent')),
                ('notes', models.TextField(null=True, verbose_name='Notes')),
            ],
            options={
                'verbose_name_plural': 'Warranties',
                'verbose_name': 'Warranty',
                'ordering': ['status_date'],
            },
        ),
        migrations.CreateModel(
            name='WarrantyColor',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('color', models.CharField(max_length=50, blank=True, verbose_name='Color')),
            ],
            options={
                'verbose_name_plural': 'Warranty Colors',
                'verbose_name': 'Warranty Color',
                'ordering': ['color'],
            },
        ),
        migrations.CreateModel(
            name='WarrantyHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('action', models.CharField(max_length=255, verbose_name='Action')),
                ('action_date', models.DateTimeField(verbose_name='Action Date', auto_now_add=True)),
                ('user_profile', models.ForeignKey(to='db.UserProfile', verbose_name='User Profile', related_name='warranty_history')),
                ('warranty', models.ForeignKey(to='db.Warranty', verbose_name='Warranty', related_name='warranty_history')),
            ],
            options={
                'verbose_name_plural': 'Warranty History',
                'verbose_name': 'Warranty History',
                'ordering': ['action_date'],
            },
        ),
        migrations.CreateModel(
            name='WarrantyImage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('type', models.CharField(max_length=20, choices=[('PROOF', 'Proof of Purchase'), ('IMAGE', 'Product Image')], default='PROOF')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('file_path', models.FileField(upload_to=db.models.warranty_image.get_file_path_upload_to)),
                ('file_name', models.CharField(max_length=50, null=True, verbose_name='File Name')),
                ('file_extension', models.CharField(max_length=10, null=True, verbose_name='File Extension')),
                ('description', models.CharField(max_length=255, null=True, verbose_name='Description')),
                ('uploaded', models.DateField(auto_now_add=True)),
                ('warranty', models.ForeignKey(null=True, to='db.Warranty', related_name='images')),
            ],
            options={
                'verbose_name_plural': 'Warranty Images',
                'verbose_name': 'Warranty Image',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='WarrantyStyle',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('style', models.CharField(max_length=50, blank=True, verbose_name='Style')),
            ],
            options={
                'verbose_name_plural': 'Warranty Styles',
                'verbose_name': 'Warranty Style',
                'ordering': ['style'],
            },
        ),
        migrations.AddField(
            model_name='useraddress',
            name='user_profile',
            field=models.ForeignKey(null=True, to='db.UserProfile', related_name='addresses'),
        ),
        migrations.AddField(
            model_name='productitem',
            name='product_style',
            field=models.ForeignKey(null=True, to='db.ProductStyle', verbose_name='Product Style', related_name='product_items'),
        ),
        migrations.AddField(
            model_name='order',
            name='user_profile',
            field=models.ForeignKey(null=True, to='db.UserProfile', related_name='orders'),
        ),
        migrations.AddField(
            model_name='modelinventory',
            name='user_profile',
            field=models.ForeignKey(null=True, to='db.UserProfile', related_name='model_inventory'),
        ),
        migrations.AddField(
            model_name='buyer',
            name='user_profile',
            field=models.ForeignKey(to='db.UserProfile', related_name='buyers'),
        ),
    ]
