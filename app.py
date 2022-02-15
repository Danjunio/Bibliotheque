from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:root@localhost:5432/api'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hjxmhzdcobywnv:4eea5de9b9f5c0a384d3e82e5bb0e65d06f9e630082cbb8f12c828b3d65d9573@ec2-52-73-149-159.compute-1.amazonaws.com:5432/d1f54elmspndr0'
db = SQLAlchemy(app)

@app.route('/')
def index():
	return '<h2>Hey! WELCOME</h2> <br> this is API for your librabry'



@app.route('/livres/',methods=["GET"])
def get_books():
	d = {}
	l = list()
	x = 0
	query = Livre.query.all()
	for livre in query:
		
		l.append({'id':livre.id,'code':livre.code,'titre':livre.titre,'datePublication':livre.datePublication,'categorie_id':livre.categorie_id,'nomAuteur':livre.nomAuteur,'nomEditeur':livre.nomEditeur})
		x = x + 1
	d["succes"] = "OK"
	d["livres"] = l
	return d
@app.route('/categories/',methods=["GET"])
def get_categories():
	d = {}
	l = list()
	x = 0
	query = Categorie.query.all()
	for c in query:
		l.append({'id':c.id,'libelle':c.libelle})
	d["succes"] = "OK"
	d["categories"] = l
	return d
	


@app.route('/livre/<int:id>')
def get_livre(id):
	livre = Livre.query.all()
	for i in livre:
		if i.id == id:
			return({"livre":{"id":i.id,"code":i.code,"titre":i.titre,"datePublication":i.datePublication,"categorie_id":i.categorie_id,"nomAuteur":i.nomAuteur,"nomEditeur":i.nomEditeur},"message":"Found","succes":"OK"})
	
	return ({"message":"Not Found","succes":" NOT OK"})


@app.route('/livre/<int:id>',methods=["DELETE"])
def delete_livre(id):
	try:
		i = Livre.query.filter_by(id=id)
		i_ = i[0]
		i.delete()
		db.session.commit()
		return ({"livre":{"id":i_.id,"code":i_.code,"titre":i_.titre,"datePublication":i_.datePublication,"categorie_id":i_.categorie_id,"nomAuteur":i_.nomAuteur,"nomEditeur":i_.nomEditeur},"success":"OK","deleted":"True"})
	except Exception as e:
		print(e)
		pass
	return ({"message":"l'id n'existe pas","succes":"NOT OK","deleted":"False"})


@app.route('/livreUpdate/',methods=["PUT"])
def update_livre():
	try:
		b_d = json.loads(request.data.decode())
		c = Livre.query.filter_by(id = b_d["id"])
		if c == None or c.count() == 0:
			return ({"success":"False","Erreur":"l'id du livre n'existe pas"})

		for key in b_d:
			Livre.query.filter_by(id=b_d['id']).update({key:b_d[key]})
		db.session.commit()
		return ({"success":"OK","Message":"Livre Mise a Jour"})
	except:
		return ({"message":"une erreur est survenus"})
	




@app.route('/categorie/<int:id>')
def get_categorie(id):
	categorie = Categorie.query.all()
	for c in categorie:
		if c.id == id:
			return({"succes":"OK","categorie":{"id":c.id,"libelle":c.libelle}})
	return ({"message":"Not Found","succes":" NOT OK"})


@app.route('/categorie/<int:id>',methods=["DELETE"])
def delete_categorie(id):
	try:
		c = Categorie.query.filter_by(id=id)
		c_ = c[0]
		c.delete()
		db.session.commit()
		return ({"Categorie":{"id":c_.id,"libelle":c_.libelle},"deleted":"True","success":" OK"})
	except Exception as ex:
		print(ex)
		return ({"deleted":"False","success":"NOT OK"})
		
@app.route('/categorieUpdate/',methods=["PUT"])
def update_categorie():
	b_d = json.loads(request.data.decode())
	c = Categorie.query.filter_by(id = b_d["id"])
	if c == None or c.count() == 0:
		return ({"success":"False","Erreur":"l'id n'existe pas"})
	for key in b_d:
		Categorie.query.filter_by(id=b_d['id']).update({key:b_d[key]})
	db.session.commit()
	return ({"success":"True","Message":"Categorie Mise a Jour"})
	


	


@app.route('/categorie/<int:id>/livres/')
def get_categorie_livre(id):
	d = {}
	li = list()
	#categorie = Categorie.query.all()
	livre = Livre.query.all()
	for i in livre:
		if id == i.categorie_id:
			li.append({"id":i.id,"code":i.code,"titre":i.titre,"datePublication":i.datePublication,"categorie_id":i.categorie_id,"nomAuteur":i.nomAuteur,"nomEditeur":i.nomEditeur})
	d["categorie"] = id
	d["livres"] = li
	d["success"] = "OK"
	return d
	#return ({"message":"Not Found"})



@app.route('/ajouter/livre/',methods=["POST"])
def ajouter_livre():
	try:
		
		book_data = json.loads(request.data.decode())
		livrex = Livre(code=book_data['ISBN'],titre=book_data['titre'],datePublication=book_data['datePublication'],categorie_id=book_data['categorie_id'],nomAuteur=book_data['nomAuteur'],nomEditeur=book_data['nomEditeur'])
	
		db.session.add(livrex)
		db.session.commit()
		return {"message":"livre ajouter"}
	except:
		return {"message":"livre non ajouter"}
	
@app.route('/ajouter/categorie',methods=["POST"])
def ajouter_categorie():
	try:
		categorie_data = json.loads(request.data.decode())
		categorie = Categorie(id=categorie_data["id"],libelle=categorie_data["libelle"])
		db.session.add(categorie)
		db.session.commit()
		return {"message":"categorie ajouter"}
	except:
		return {"message":"categorie non ajouter"}
	

class Categorie(db.Model):
	__tablename__ = 'categories'
	id = db.Column(db.Integer,primary_key=True)
	libelle = db.Column(db.String,nullable=False)
	livre = db.relationship("Livre",backref="categories",lazy=True)

#db.create_all()

class Livre(db.Model):
	__tablename__ = 'livres'
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	code = db.Column(db.String,nullable=False)
	titre = db.Column(db.String,nullable=False)
	datePublication = db.Column(db.Date,nullable=False)
	categorie_id = db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=False)
	nomAuteur = db.Column(db.String,nullable=False)
	nomEditeur = db.Column(db.String,nullable=False)


db.create_all()

#port = int(os.environ.get("PORT", 5000))
#app.run(host="0.0.0.0", port=port)
# s Livre(db.Model):
if __name__ == "__main__":
	app.run()
