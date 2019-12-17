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

    def __str__(self):
        return 'Produit: {}'.format(self.codeProduit, self.familleProduit, self.descriptionProduit, self.quantiteMin, self.packaging, self.prix)

class Customer(models.Model):
    IdClient = models.TextField(blank=False)
    Nom = models.CharField(max_length=200)
    Prenom = models.CharField(max_length=200)
    Credit = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    Paiement = models.IntegerField(default=0)
    Compte = models.CharField(max_length=10, default="")
    carteFid = models.IntegerField(default=-1)

    def __str__(self):
        return 'Customer: {}'.format(self.firstName, self.lastName, self.fidelityPoint, self.payment, self.account)


class PurchasedArticle(models.Model):
    codeProduit = models.CharField(max_length=200)
    prixAvant = models.IntegerField(default=0)
    prixApres = models.IntegerField(default=0)
    promo = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    ticket = models.ForeignKey('Ticket', related_name='purchased_articles', on_delete=models.CASCADE)

class Ticket(models.Model):
    DateTicket = models.DateField(blank=True, null=True)
    Prix = models.IntegerField(default=0)
    Client = models.TextField(blank=False)
    PointsFidelite = models.IntegerField(default=0)
    ModePaiement = models.CharField(max_length=10)

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