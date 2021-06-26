from flask import Flask,render_template,redirect,url_for,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
from models import users,urls
import os
import requests
import core.priceConvertison.main as c
import core.scarper.main as scrape


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Changing Environment Development Environment and Deployment Environment.
 
ENV = 'dev'

if ENV == 'dev':
    
    app.debug=True
    POSTGRES = {
    'user': 'postgres',
    'pw': 'root',
    'db': 'tracker',
    'host': 'localhost',
    'port': '5432',
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

else:
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://shnrnzzcnnlnoh:3c9284ca6e9d50087fbadfa1ff2b9554afe6b27abb0d3b841f11416133cf2dc6@ec2-54-163-97-228.compute-1.amazonaws.com:5432/da473kgjmj461l'
    app.debug = True




               

def passwordValidation(username,password):
    data = users.query.filter_by(username=username).first()
    if data.password == password:
        return True,data.user_id
    return False
    

def geturl(id):
    data = urls.query.filter_by(user_id = id)
    return list(data)


@app.route("/",methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/dashboard",methods=["GET"])
def dashboard():
    
    data = geturl(session['user']) 
    new_data = []
    
    for i in data:
        id = i.url_id
        product,price = scrape(i.url)
        reqprice = i.price
        reqprice = c.converter(reqprice)
        new_data.append([product,price,reqprice,id])
    return render_template("dashboard.html",data=new_data)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        if username == "" or password == "":
            return render_template("index.html",message="Enter all the fields")
        valid,id = passwordValidation(username,password)
        
        if valid:
            session['user'] = id
            return redirect(url_for("dashboard"))
            
    return render_template("index.html")


@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        phno = request.form['phno']
        password = request.form['password']
        
        if username == "" or password == "":
            return render_template("index.html",message="Enter all the fields")
        
        if db.session.query(users).filter(users.username == username).count() == 0:
            data = users(username,email,phno,password)
            db.session.add(data)
            db.session.commit()
            return render_template("index.html",x=True)
        
        else : return render_template("index.html",x=False)      
            
    return render_template("index.html")



@app.route("/addurl",methods=["GET","POST"])
def addurl():
    if request.method == "POST":
        url = request.form['url']
        price = request.form['price']
        data = urls(session['user'],url,price)
        db.session.add(data)
        db.session.commit()
    return redirect(url_for("dashboard"))







if __name__ == "__main__":
    app.secret_key = os.getenv("SECRET_KEY")
    app.run(debug=True)