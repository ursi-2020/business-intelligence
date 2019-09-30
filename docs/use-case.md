[Sommaire](https://ursi-2020.github.io/business-intelligence/)

Le rôle de Business Intelligence (ou informatique décisionnelle), est de fournir l’analyse des données du SI en rendant les informations exploitables aux gestionnaires d’entreprises et autres utilisateurs sans spécialisation technique de prendre des décisions.

L'objectif de ce premier rendu étant de disposer d'une base pour afficher les données des applications Catalogue Produit et CRM et dans un futur proche toutes les autres.

## Business intelligence -> Catalogue produits

### Récupérer l'ensemble des produits du Catalogue

<!---![Diagramme de séquence](./usecase_produits.svg) -->

Ce diagramme de séquence montre comment l'application BI récupère l'ensemble des produits disponibles dans le Catalogue Produits.

![Diagramme de séquence](./sequence_produit.png)

L'application business-intelligence commence par demander la liste des produits disponibles auprès du Catalogue Produits.
Ce dernier nous renvoie un objet JSON contenant un tableau des produits disponibles.

Appel vers le catalogue:

```python
products = api.send_request("catalogue-produit", "api/data")
data = json.loads(products)
```

Ex de JSON reçu:

```json
{
    produits: [
        {
            id : 1,
            codeProduit: "X1-0",
            descriptionProduit: "Frigos:P1-0",
            familleProduit : "Frigos",
            packaging : 2,
            prix : 424,
            quantiteMin : 15
        }
    ]
}
```

### Enregistrement des données produits

Une fois le JSON reçu, nous enregistrons dans notre BDD l'ensemble des produits, à l'aide de ce code:

```python
for product in json_data["produits"]:
        if not Produit.objects.filter(codeProduit=product["codeProduit"]).exists():
            new_product = Produit(codeProduit=product["codeProduit"], familleProduit=product["familleProduit"], descriptionProduit=product["descriptionProduit"], quantiteMin=product["quantiteMin"], packaging=product["packaging"], prix=product["prix"])
            new_product.save()
    return catalogue_produit(request)
```

### Afficher les données récupérées

Il est possible d'afficher les données récupérées sous forme de plusieurs tableau en récupérant les données de donne BDD de cette manière:

```python
def catalogue_produit(request):
    products = Produit.objects.all()
    return render(request, "catalogue_produit.html", {'products': products})
```

## BI -> CRM

Les fonctions utilisées pour récupérer les données de l'application CRM sont identiques à celles de Catalogue Produit, de même que pour les afficher.


