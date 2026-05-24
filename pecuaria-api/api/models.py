from django.db import models

class Dono(models.Model):
    id_dono = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    usuario = models.CharField(max_length=15, unique=True)
    senha = models.CharField(max_length=128)
    status_dono = models.CharField(max_length=1) 
    telefone = models.CharField(max_length=15, null=True, blank=True)
    cor_brinco = models.CharField(max_length=20, null=True, blank=True)
    descricao_marca = models.CharField(max_length=150, null=True, blank=True)
    perfil = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'dono'
        managed = False

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=150)
    nome_categoria = models.CharField(max_length=1) 

    class Meta:
        db_table = 'categoria'
        managed = False

class Leilao(models.Model):
    id_leilao = models.AutoField(primary_key=True)
    nome_evento = models.CharField(max_length=150)
    dt_leilao = models.DateField()
    custo_fixo = models.DecimalField(max_digits=8, decimal_places=2)
    local = models.CharField(max_length=150, null=True, blank=True) # Campo novo adicionado

    class Meta:
        db_table = 'leilao'
        managed = False

class Venda(models.Model):
    id_venda = models.AutoField(primary_key=True)
    responsavel = models.CharField(max_length=150)
    vlr_venda = models.DecimalField(max_digits=8, decimal_places=2)
    dt_venda = models.DateField()
    tp_pgto = models.CharField(max_length=1)
    id_leilao = models.ForeignKey(Leilao, on_delete=models.CASCADE, db_column='id_leilao')

    class Meta:
        db_table = 'venda'
        managed = False

class Animal(models.Model):
    id_animal = models.AutoField(primary_key=True)
    numero_brinco = models.CharField(max_length=20, null=True, blank=True)
    raca = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=1) 
    sexo = models.CharField(max_length=1)
    peso = models.DecimalField(max_digits=8, decimal_places=2)
    vlr_vendido = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dt_abate = models.DateField(null=True, blank=True)
    dt_morte = models.DateField(null=True, blank=True)
    dt_nasc = models.DateField(null=True, blank=True)
    id_dono = models.ForeignKey(Dono, on_delete=models.CASCADE, db_column='id_dono')
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria', null=True, blank=True)
    id_venda = models.ForeignKey(Venda, on_delete=models.CASCADE, db_column='id_venda', null=True, blank=True)
    id_leilao = models.ForeignKey(Leilao, on_delete=models.SET_NULL, db_column='id_leilao', null=True, blank=True) # Chave estrangeira nova adicionada

    class Meta:
        db_table = 'animal'
        managed = False