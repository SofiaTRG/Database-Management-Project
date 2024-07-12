# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actedin(models.Model):
    actor = models.CharField(db_column='Actor', primary_key=True, max_length=50)  # Field name made lowercase. The composite primary key (Actor, Title) found, that is not supported. The first column is selected.
    title = models.ForeignKey('Content', models.DO_NOTHING, db_column='Title')  # Field name made lowercase.
    salary = models.IntegerField(db_column='Salary', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ActedIn'
        unique_together = (('actor', 'title'),)


class Buying(models.Model):
    tdate = models.OneToOneField('Stock', models.DO_NOTHING, db_column='tDate', primary_key=True)  # Field name made lowercase. The composite primary key (tDate, ID, Symbol) found, that is not supported. The first column is selected.
    id = models.ForeignKey('Investor', models.DO_NOTHING, db_column='ID')  # Field name made lowercase.
    symbol = models.ForeignKey('Stock', models.DO_NOTHING, db_column='Symbol',
                               related_name='+')
    bquantity = models.IntegerField(db_column='BQuantity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Buying'
        unique_together = (('tdate', 'id', 'symbol'),)


class Company(models.Model):
    symbol = models.CharField(db_column='Symbol', primary_key=True, max_length=10)  # Field name made lowercase.
    sector = models.CharField(db_column='Sector', max_length=40, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=40, blank=True, null=True)  # Field name made lowercase.
    founded = models.IntegerField(db_column='Founded', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Company'


class Content(models.Model):
    title = models.CharField(db_column='Title', primary_key=True, max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=25, blank=True, null=True)  # Field name made lowercase.
    realese_date = models.DateField(db_column='Realese_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Content'


class Follows(models.Model):
    id1 = models.OneToOneField('Users', models.DO_NOTHING, db_column='ID1', primary_key=True)  # Field name made lowercase. The composite primary key (ID1, ID2) found, that is not supported. The first column is selected.
    id2 = models.ForeignKey('Users', models.DO_NOTHING, db_column='ID2', related_name='follows_id2_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Follows'
        unique_together = (('id1', 'id2'),)


class Interactions(models.Model):
    authorid = models.OneToOneField('Users', models.DO_NOTHING, db_column='authorID', primary_key=True)  # Field name made lowercase. The composite primary key (authorID, cNum, uID, iType) found, that is not supported. The first column is selected.
    cnum = models.IntegerField(db_column='cNum')  # Field name made lowercase.
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uID', related_name='interactions_uid_set')  # Field name made lowercase.
    itype = models.CharField(db_column='iType', max_length=8)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Interactions'
        unique_together = (('authorid', 'cnum', 'uid', 'itype'),)


class Investor(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=40, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Investor'


class Stock(models.Model):
    symbol = models.OneToOneField(Company, models.DO_NOTHING, db_column='Symbol', primary_key=True)  # Field name made lowercase. The composite primary key (Symbol, tDate) found, that is not supported. The first column is selected.
    tdate = models.DateField(db_column='tDate')  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Stock'
        unique_together = (('symbol', 'tdate'),)


class Transactions(models.Model):
    tdate = models.DateField(db_column='tDate', primary_key=True)  # Field name made lowercase. The composite primary key (tDate, ID) found, that is not supported. The first column is selected.
    id = models.ForeignKey(Investor, models.DO_NOTHING, db_column='ID')  # Field name made lowercase.
    tamount = models.IntegerField(db_column='TAmount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Transactions'
        unique_together = (('tdate', 'id'),)


class Users(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=10)  # Field name made lowercase.
    name = models.CharField(max_length=100, blank=True, null=True)
    cname = models.CharField(db_column='cName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Users'
