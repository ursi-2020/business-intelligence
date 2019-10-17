from django.db import models


class Article(models.Model):
    nom = models.CharField(max_length=200)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return 'Article: {}'.format(self.nom)


class Vente(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return 'Vente: {} - {}'.format(self.article.nom, self.date)

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
