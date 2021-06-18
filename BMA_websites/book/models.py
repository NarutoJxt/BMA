from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Book(models.Model):
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=255, blank=True, null=True)
    character_length = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey('Category', models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    img_path = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book'


class BookDetail(models.Model):
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True)
    volume = models.CharField(max_length=128, blank=True, null=True)
    section = models.CharField(max_length=64, blank=True, null=True)
    content = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'book_detail'


class Category(models.Model):
    category = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'
