from django.db import models


class Article(models.Model):
    nom = models.CharField(max_length=200)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return 'Article: {}'.format(self.nom)

class Produit(models.Model):
    codeProduit = models.CharField(max_length=200)
    familleProduit = models.CharField(max_length=200)
    descriptionProduit = models.CharField(max_length=200)
    quantiteMin = models.PositiveIntegerField()
    packaging = models.PositiveIntegerField()
    prix = models.PositiveIntegerField()
    prixFournisseur = models.PositiveIntegerField(default=0)

class Customer(models.Model):
    IdClient = models.TextField(blank=False)
    Nom = models.CharField(max_length=200)
    Prenom = models.CharField(max_length=200)
    Credit = models.IntegerField(default=0)
    Montant = models.IntegerField(default=0)
    Compte = models.CharField(max_length=10, default="")
    carteFid = models.CharField(max_length=200)
    Email = models.CharField(max_length=200, default="")
    PanierMoyen = models.IntegerField(default=0)

class PurchasedArticle(models.Model):
    codeProduit = models.CharField(max_length=200)
    prixAvant = models.IntegerField(default=0)
    prixApres = models.IntegerField(default=0)
    promo = models.IntegerField(default=0)
    promo_client_produit = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    ticket = models.ForeignKey('Ticket', related_name='purchased_articles', on_delete=models.CASCADE)

class Ticket(models.Model):
    DateTicket = models.DateField(blank=True, null=True)
    Prix = models.IntegerField(default=0)
    Client = models.TextField(blank=False)
    PointsFidelite = models.IntegerField(default=0)
    ModePaiement = models.CharField(max_length=10)
    Origin = models.CharField(default="rien", max_length=200)
    Promo_client = models.IntegerField(default=0)

class Stock(models.Model):
    date = models.DateField(blank=True, null=True)
    codeProduit = models.CharField(max_length=200)
    quantite = models.IntegerField()

    def __str__(self):
        return 'Stock: {}'.format(self.codeProduit, self.quantite)

class StockMagasin(models.Model):
    date = models.DateField(blank=True, null=True)
    codeProduit = models.CharField(max_length=200)
    numeroFournisseur = models.IntegerField()
    codeFournisseur = models.CharField(max_length=200)
    stockDisponible = models.IntegerField()

class Delivery(models.Model):
    type = models.CharField(max_length=200)
    idCommande = models.CharField(max_length=200)

class DeliveredProduct(models.Model):
    codeProduit = models.CharField(max_length=200)
    quantite = models.IntegerField(default=0)
    delivery = models.ForeignKey('Delivery', related_name='delivered_product', on_delete=models.CASCADE)

class Result(models.Model):
    type = models.CharField(max_length=200)
    value = models.IntegerField(default=0)
    date = models.DateField(blank=True, null=True)

class Incident(models.Model):
    client_id = models.TextField()
    amount = models.IntegerField(default=0)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return 'Incident: {}'.format(self.date)

class Facture(models.Model):
    numeroFacture = models.CharField(max_length=200)
    dateFacture = models.DateField(blank=True, null=True)
    datePaiement = models.DateField(blank=True, null=True)
    numeroCommande = models.CharField(max_length=200)
    dateLivraison = models.DateField(blank=True, null=True)

class FactureItem(models.Model):
    codeProduit = models.CharField(max_length=200)
    prix = models.IntegerField(default=0)
    quantite = models.IntegerField(default=0)
    facture = models.ForeignKey('Facture', related_name='facture_item', on_delete=models.CASCADE)