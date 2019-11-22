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

class Vente(models.Model):
    date = models.DateTimeField()
    prix = models.IntegerField(default=0)
    client = models.CharField(max_length=20, default="")
    pointsFidelite = models.IntegerField(default=0)
    modePaiement = models.CharField(max_length=10, default= "")
    articles = models.ManyToManyField(Produit, through='ArticleVendu')

class ArticleVendu(models.Model):
    article = models.ForeignKey(Produit, on_delete=models.PROTECT)
    vente = models.ForeignKey(Vente, on_delete=models.PROTECT)
    quantity = models.IntegerField(null=True)
    prixAvant = models.IntegerField(null=True)
    prixApres = models.IntegerField(null=True)
    promo = models.IntegerField(null=True)
