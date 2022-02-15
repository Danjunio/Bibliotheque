import os
from flask_sqlalchemy import SQLAlchemy
import json

from flask import Flask, abort, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy  # importer SQLAlchemy
import urllib.parse
from urllib.parse import quote_plus


app = Flask(__name__)  

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:{}@localhost:5432/my_api".format(
'root')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hjxmhzdcobywnv:4eea5de9b9f5c0a384d3e82e5bb0e65d06f9e630082cbb8f12c828b3d65d9573@ec2-52-73-149-159.compute-1.amazonaws.com:5432/d1f54elmspndr0'
# connexion à la base de données
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Créer une instance de BD


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


########### Categorie
class Categorie(db.Model):
    __tablename__ = 'categories'
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    libelle_categorie=db.Column(db.String(30),nullable=False)
    livres=db.relationship('Livre',backref='categories', lazy=True)
    def __init__(self, libelle_categorie):
        #self.id = id
        self.libelle_categorie = libelle_categorie
       

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'libelle_categorie': self.libelle_categorie

        }

db.create_all()


########### Categorie

class Livre(db.Model):
    __tablename__ = 'livres'
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    isbn=db.Column(db.String,nullable=False )
    titre=db.Column(db.String(30),nullable=False)
    date_publication=db.Column(db.Date,nullable=False)
    auteur=db.Column(db.String(100),nullable=False)
    editeur=db.Column(db.String(100),nullable=True)
    categorie_id=db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=False)

    def __init__(self, isbn,titre,date_publication,auteur,editeur,categorie_id):
        #self.id = id
        self.isbn = isbn
        self.titre = titre
        self.date_publication = date_publication
        self.auteur = auteur
        self.editeur = editeur
        self.categorie_id = categorie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'isbn': self.isbn,
            'titre': self.titre,
            'date_publication': self.date_publication,
            'auteur': self.auteur,
            'titre': self.categorie_id,
        }


db.create_all()


#############
############# ROUTES
#############

@app.route('/')
def index():
	return '<h2>Hey! WELCOME</h2> <br> this is API for your librabry'

#################################################
#           Liste des livres \catégories
####################################################


@app.route('/livres',methods=["GET"])
def get_all_book():
    livre = Livre.query.all()
    livre = [p.format() for p in livre]
    return jsonify(
        {
            'success': True,
            'livre': livre,
            'nombre': len(Livre.query.all())}
    )
########### Categorie
@app.route('/categories',methods=["GET"])
def get_all_categorie():
    categorie = Categorie.query.all()
    categorie = [p.format() for p in categorie]
    return jsonify(
        {
            'success': True,
            'categorie': categorie,
            'nombre': len(Categorie.query.all())}
    )


#################################################
#           selectioner un livre \ catégorie
####################################################

@app.route('/livre/<int:id>')
def get_livre(id):
	livre = Livre.query.all()
	for i in livre:
		if i.id == id:
			return({"livre":{"id":i.id,
                    "code":i.isbn,
                    "titre":i.titre,
                    "datePublication":i.date_publication,
                    "categorie_id":i.categorie_id,
                    "nomAuteur":i.auteur,
                    "nomEditeur":i.editeur},"message":"Found","succes":"OK"})
	
	return ({"message":"Not Found","succes":" NOT OK"})

        
########### categorie

@app.route('/categorie/<int:id>')
def get_categorie(id):
	categorie = Categorie.query.all()
	for c in categorie:
		if c.id == id:
			return({"succes":"OK",
           "categorie":{"id":c.id,"libelle":c.libelle_categorie}})
	return ({"message":"Not Found","succes":" NOT OK"})


#################################################
#           Ajouter un livre \ catégorie
####################################################


# @app.route('/livres', methods=['POST'])
# def add_livre():
#     body = request.get_json()
    
#     new_isbn = body.get('isbn', None)
#     new_titre = body.get('titre', None)
#     new_date_publication = body.get('date_publication', None)
#     new_auteur = body.get('auteur', None)
#     new_editeur = body.get('editeur', None)
#     new_categorie_id = body.get('categorie_id', None)
#     livre = Livre(isbn=new_isbn, titre=new_titre, date_publication=new_date_publication, auteur=new_auteur, editeur=new_editeur, categorie_id=new_categorie_id)
#     livre.insert()
#     livres = Livre.query.all()
#     livres_formatted = [p.format() for p in livres]
#     return jsonify({
#         'success': True,
#         'created': livre.id,
#         'livres': livres_formatted,
#         'total_livres': len(Livre.query.all())
#     })
    

########### Categorie


# @app.route('/categories', methods=['POST'])
# def add_categorie():
#     body = request.get_json()
#     new_libelle_categorie = body.get('libelle_categorie', None)
#     new_id = body.get('id', None)
#     categorie = Categorie(libelle_categorie=new_libelle_categorie)
#     categorie.insert()
#     categories = Categorie.query.all()
#     categories_formatted = [p.format() for p in categories]
#     return jsonify({
#         'success': True,
#         'created': categorie.id,
#         'categories': categories_formatted,
#         'total_categories': len(Categorie.query.all())
#     })


#################################################
#          lister une catégorie
####################################################






#################################################
#           Modifier un livre \ catégorie
####################################################


@app.route('/livres/<int:livre_id>', methods=['PATCH'])
def update_livre(livre_id):
    body = request.get_json()
    try:
        mon_livre = Livre.query.filter(Livre.id == livre_id).one_or_none()
        if mon_livre is None:
            abort(404)
        if 'isbn' in body and 'titre' in body and  'date_publication' in body and 'auteur' in body and  'editeur' in body and 'categorie_id' in body:
            mon_livre.isbn = body.get('isbn')
            mon_livre.titre = body.get('titre')
            mon_livre.date_publication = body.get('date_publication')
            mon_livre.auteur = body.get('auteur')
            mon_livre.editeur = body.get('editeur')
            mon_livre.categorie_id = body.get('categorie_id')
        mon_livre.update()
        return jsonify({
            'success': True,
            'id': mon_livre.id,
            'livre_modifie': mon_livre.format()
        })
    except:
        abort(400)
        
########### Categorie

@app.route('/categories/<int:categorie_id>', methods=['PATCH'])
def update_categorie(categorie_id):
    body = request.get_json()
    try:
        ma_categorie = Categorie.query.filter(Categorie.id == categorie_id).one_or_none()
        if ma_categorie is None:
            abort(404)
        if 'libelle_categorie' in body:
            ma_categorie.libelle_categorie = body.get('libelle_categorie')
       
        ma_categorie.update()
        return jsonify({
            'success': True,
            'id': ma_categorie.id,
            'livre_modifie': ma_categorie.format()
        })
    except:
        abort(400)


#################################################
#           Supprimer un livre \ catégorie
#################################################
@app.route('/livres/<int:livre_id>', methods=['DELETE'])
def supprimer_livre(livre_id):
    try:
        mon_livre = Livre.query.get(livre_id)
        if mon_livre is None:
            abort(404)
        else:
            mon_livre.delete()
            return jsonify({
                "success": True,
                "deleted_id": livre_id,
                "total_livres": len(Livre.query.all())
            })
    except:
        abort(400)
    finally:
        db.session.close()
        
########### Categorie
      
@app.route('/categories/<int:categorie_id>', methods=['DELETE'])
def supprimer_categorie(categorie_id):
    try:
        ma_categorie = Categorie.query.get(categorie_id)
        if ma_categorie is None:
            abort(404)
        else:
            ma_categorie.delete()
            return jsonify({
                "success": True,
                "deleted_id": ma_categorie,
                "total_categorie": len(Categorie.query.all())
            })
    except:
        abort(400)
    finally:
        db.session.close()
        
        
#################################################
#           Liste des livres d'une catégories
####################################################
@app.route('/categories/<int:id>/livres')
def book_categorie(id):
    try:
        categorie = Categorie.query.get(id)
        livres = Livre.query.filter_by(categorie_id=id).all()
        livres = [p.format() for p in livres]
        return jsonify(
            {
                'success': True,
                'nombre':len(livres),
                'statut_code': 200,
            }
        )
    except :
        abort(404)
    finally:
        db.session.close()

#ici on fait un get et la ressource 
#n'existe pas http://localhost:5000/persons/200
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404
    
@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal server error"
        }), 500
    
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad Request"
        }), 400

if __name__ == "__main__":
	app.run()
