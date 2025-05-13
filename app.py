#Configuration des templates avec app.py

from flask import Flask, request, render_template, redirect  #importer Flask, render_template, et redirect depuis le module flask
#from flask import request, redirect, url_for #importer request, redirect et url_for depuis le module flask
#flask est un micro-framework pour Python qui permet de créer des applications web rapidement et facilement.
from flask_sqlalchemy import SQLAlchemy #importer SQLAlchemy pour la gestion de la base de données
from datetime import datetime #importer pour avoir la date de creation des tables 

app = Flask(__name__) #creer une instance de l'application Flask
app.config['QLALCHEMY_TRACK_MODIFICATIONS'] = False #désactiver le suivi des modifications de SQLAlchemy pour éviter les avertissements inutiles.
#magic_methodes => __repr__ (représentation de l'objet), __init__ (initialisation de l'objet), __str__ (conversion de l'objet en chaîne de caractères)
# __name__ est une variable spéciale qui contient le nom du module actuel

#premiere configuration => renseigner l'url de la base de données
#SQLAlchemy est une bibliothèque Python qui facilite l'interaction avec les bases de données relationnelles.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db' #configuration de la base de données SQLite
#'sqlite:///budget.db' => chemin vers le fichier de base de données SQLite. Le triple slash (///) indique que le fichier est situé dans le même répertoire que le script Python.
#///budget.db =>nom de la base de données SQLite. Si le fichier n'existe pas, il sera créé automatiquement.

#declarer l'instance de SQLAlchemy
db = SQLAlchemy(app) #créer une instance de SQLAlchemy en lui passant l'application Flask comme argument. Cela permet à SQLAlchemy de gérer la base de données pour cette application.
#SQLAlchemy est un ORM (Object-Relational Mapping) qui permet de travailler avec des bases de données relationnelles en utilisant des objets Python au lieu d'écrire des requêtes SQL directement.


#Creer une table
#table => permet de créer une nouvelle table dans la base de données. Elle définit les colonnes et les types de données de la table.
#Elle est utilisée pour définir la structure de la base de données et les relations entre les tables.

#class => permet de créer une nouvelle classe en Python. Une classe est un modèle pour créer des objets.
#Elle définit les attributs et les méthodes que ces objets auront.
#class Task(db.Model): #définir une nouvelle classe Task qui hérite de db.Model. Cela signifie que Task est un modèle de base de données.
   # id = db.Column(db.Integer, primary_key=True) #id => colonne id de type entier (Integer) qui est la clé primaire (primary_key=True) de la table. Cela signifie que chaque enregistrement dans la table aura un identifiant unique.
   # name = db.Column(db.String(80), nullable=False) #title => colonne title de type chaîne de caractères (String) avec une longueur maximale de 100 caractères. nullable=False signifie que cette colonne ne peut pas être vide.
    #date_created = db.Column(db.DateTime, nullable=False,default=datetime.utcnow) #date_created => colonne date_created de type DateTime qui stocke la date et l'heure de création de l'enregistrement. default=datetime.utcnow signifie que la valeur par défaut sera la date et l'heure actuelles.

   # def __repr__(self): #méthode spéciale qui définit comment l'objet sera représenté sous forme de chaîne de caractères.
        #return '<Task %r>' % self.id #renvoie une chaîne contenant l'identifiant de la tâche.
#Cette méthode est utilisée pour afficher des informations sur l'objet lorsque vous l'imprimez ou le journalisez.


class Depense(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    titre = db.Column(db.String(80), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,default=datetime.utcnow) 
    def __repr__(self): 
        return '<Depense %r>' % self.id 

class Revenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80), nullable=False) 
    montant = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,default=datetime.utcnow) 
    def __repr__(self): 
        return '<Revenu %r>' % self.id 

@app.route('/') #decorateur pour definir la route de l'application
def index():
    depenses = Depense.query.order_by(Depense.date_created.desc()).all() #query => méthode de SQLAlchemy qui permet d'interroger la base de données. order_by(Depense.date_created.desc()) => trie les résultats par date de création dans l'ordre décroissant (desc()). all() => récupère tous les enregistrements de la table Depense.
    revenus = Revenu.query.order_by(Revenu.date_created.desc()).all() #query => méthode de SQLAlchemy qui permet d'interroger la base de données. order_by(Revenu.date_created.desc()) => trie les résultats par date de création dans l'ordre décroissant (desc()). all() => récupère tous les enregistrements de la table Revenu.
    #query.all() => méthode de SQLAlchemy qui récupère tous les enregistrements de la table Depense et Revenu. Elle renvoie une liste d'objets Depense et Revenu.
    budget = 0  
    for depense in depenses:  
            budget -= depense.montant 
    for revenu in revenus:  
            budget += revenu.montant  
    budget = sum(revenu.montant for revenu in revenus) - sum(depense.montant for depense in depenses) 
    
    depenses_total=sum(depense.montant for depense in depenses) 
    solde=budget-depenses_total 
    
    return render_template('index.html',depenses=depenses,revenus=revenus,budget=budget,depenses_total=depenses_total,solde=solde) #render_template => fonction de Flask qui rend un template HTML et le renvoie au client. Elle prend en paramètre le nom du fichier HTML à rendre.
   
# Le fichier HTML doit être placé dans le dossier templates de l'application Flask.
 #check pour demander si le main est egale a __name__ (si le script est exécuté directement)


@app.route('/supprimer_depense/<int:id>') 
def supprimer(id):
    depenses = Depense.query.get_or_404(id)
    #get_or_404(id) => méthode de SQLAlchemy qui récupère un enregistrement par son identifiant (id). Si l'enregistrement n'existe pas, elle renvoie une erreur 404.
    try:
        db.session.delete(depenses) #delete(depenses) => méthode de SQLAlchemy qui supprime l'enregistrement de la session de la base de données.
        db.session.commit() #commit() => méthode de SQLAlchemy qui valide la session de la base de données pour enregistrer les modifications.
        return redirect('/')
    except Exception:
        return "Erreur lors de la suppression "
    

app.route('/supprimer_revenu/<int:id>')
def supprimer_revenu(id):
    revenus = Revenu.query.get_or_404(id) 
    try:
        db.session.delete(revenus)
        db.session.commit() 
        return redirect('/')
    except Exception:
        return "Erreur lors de la suppression "
    

app.route('/modifier_depense/<int:id>', methods=["GET","POST"]) 
def modifier_depense(id):
    depenses = Depense.query.get_or_404(id) 
    if request.method == "POST":
        depenses.titre = request.form.get('titre') #recuperer le titre du formulaire
        depenses.montant = request.form.get('montant') #recuperer le montant du formulaire
        try:
            db.session.commit() 
            return redirect('/')
        except Exception:
            return "Erreur lors de la modification de la depense"
    return render_template('modifier_depense.html',depenses=depenses)


app.route('/modifier_revenu/<int:id>', methods=["GET","POST"])
def modifier_revenu(id):
    revenus = Revenu.query.get_or_404(id) 
    if request.method == "POST":
        revenus.titre = request.form.get('titre') 
        revenus.montant = request.form.get('montant') 
        try:
            db.session.commit() 
            return redirect('/')
        except Exception:
            return "Erreur lors de la modification du revenu"
    return render_template('modifier_revenu.html',revenus=revenus)

@app.route('/depense/', methods=["GET","POST"]) #decorateur pour definir la route de l'application
#@app.route('/depense') => définit une nouvelle route pour l'application Flask. Lorsque l'utilisateur accède à l'URL '/depense', la fonction def() sera exécutée.
def depense():
    if request.method == "POST": #verifier toujours si la methode de la requete est POST
        #recuperer les donnees du formulaire
        titre = request.form.get('titre') #recuperer le titre du formulaire
        montant = request.form.get('montant') #recuperer le montant du formulaire
        nouveau_depense = Depense(titre=titre, montant=montant) #creer une nouvelle depense avec le titre et le montant recuperes du formulaire
        try:
            db.session.add(nouveau_depense) #ajouter la nouvelle depense a la session de la base de donnees
            db.session.commit() #valider la session de la base de donnees pour enregistrer la nouvelle depense
            return redirect('/')
        except  Exception:
            return "Erreur lors de l'ajout de la depense" 
        
    else:
        depenses = Depense.query.order_by(Depense.date_created.desc()).all() #query => méthode de SQLAlchemy qui permet d'interroger la base de données. order_by(Dépense.date_created.desc()) => trie les résultats par date de création dans l'ordre décroissant (desc()). all() => récupère tous les enregistrements de la table Depense.
    #query.order_by(Depense.date_created.desc()) => méthode de SQLAlchemy qui trie les résultats de la requête par date de création dans l'ordre décroissant (desc()). Cela signifie que les enregistrements les plus récents apparaîtront en premier.

    return render_template('depense.html',depenses=depenses)




@app.route('/revenu/', methods=["GET","POST"]) #decorateur pour definir la route de l'application
def revenu():
    if request.method =="POST":
        titre = request.form.get('titre')
        montant = request.form.get('montant')
        nouveau_revenu = Revenu(titre=titre, montant=montant) 
        try:
            db.session.add(nouveau_revenu) 
            db.session.commit()
            return redirect('/')
        except  Exception:
            return "Erreur lors de l'ajout du revenu"
    else:
        revenus = Revenu.query.order_by(Revenu.date_created.desc()).all() #query => méthode de SQLAlchemy qui permet d'interroger la base de données. order_by(Revenu.date_created.desc()) => trie les résultats par date de création dans l'ordre décroissant (desc()). all() => récupère tous les enregistrements de la table Revenu.
    #query.all() => méthode de SQLAlchemy qui récupère tous les enregistrements de la table Depense et Revenu. Elle renvoie une liste d'objets Depense et Revenu.

    return render_template('revenu.html',revenus=revenus) 



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) #lance l'application en mode debug (recharge automatique des modifications)
#app.run() => lance le serveur de développement intégré de Flask. Le paramètre debug=True active le mode débogage, ce qui permet de recharger automatiquement l'application lorsque des modifications sont apportées au code.
# Cela facilite le développement en permettant de voir les changements sans avoir à redémarrer manuellement le serveur.
# Le serveur écoute par défaut sur le port 5000, mais vous pouvez spécifier un autre port en ajoutant le paramètre port=XXXX dans la méthode run().N

#create_all() => méthode de SQLAlchemy qui crée toutes les tables définies dans les modèles de la base de données. Elle vérifie si les tables existent déjà et ne les recrée pas si elles existent.
#app.app_context() => crée un contexte d'application Flask. Cela permet d'accéder à l'application et à la base de données dans le bloc de code qui suit. C'est nécessaire pour exécuter des opérations sur la base de données en dehors des routes de l'application.
#les methodes post et get => sont des méthodes HTTP utilisées pour envoyer et recevoir des données entre le client et le serveur.
# La méthode GET est utilisée pour demander des données au serveur, tandis que la méthode POST est utilisée pour envoyer des données au serveur.    
#la methode post est utilisée pour envoyer des données au serveur, tandis que la méthode get est utilisée pour récupérer des données du serveur.
# La méthode POST est généralement utilisée pour soumettre des formulaires, tandis que la méthode GET est utilisée pour récupérer des ressources.