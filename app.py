from flask import Flask,render_template,redirect,url_for,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
import requests
from bs4 import BeautifulSoup



app = Flask(__name__)

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

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class users(db.Model):
    
    __tablename__ = 'users'
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    emailid = db.Column(db.String(100), unique=True)
    phoneno = db.Column(db.String(12), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,username,emailid,phoneno,password):
        self.username = username
        self.emailid = emailid
        self.phoneno = phoneno
        self.password = password
        
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated
               

def passwordValidation(username,password):
    data = users.query.filter_by(username=username).first()
    if data.password == password:
        return True,data.user_id
    
    #print(password,users.password)
    return False
    
    
    
    
class urls(db.Model):
    
    __tablename__ = 'urls'
    url_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    url = db.Column(db.Text)
    price = db.Column(db.Integer)

    def __init__(self,user_id,url,price):
        self.user_id = user_id
        self.url = url
        self.price = price


def geturl(id):
    
    data = urls.query.filter_by(user_id = id)
    return list(data)


@app.route("/")
def home():
    return render_template("index.html",x=False)


@app.route("/dashboard")
def dashboard():
    data = geturl(session['user'])
    new_data = []
    for i in data:
        product,price = scrape(i.url)
        reqprice = i.price
        new_data.append([product,price,reqprice])
    print(new_data)
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
            #print(session['user'])
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
    

header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}



##############################################################################################################
#                                                                                                            #
#                               Scraping Method .                                                            #
#                                                                                                            #
# To get product inside the url by using "id" : "productTitle" .                                             #           
# To get price of product inside the url by using "id":"priceblock_ourprice" or "id":"priceblock_dealprice" .#
#                                                                                                            #
##############################################################################################################
def scrape(url):
    page = requests.get(url,headers=header)
    soup = BeautifulSoup(page.content,'html.parser')
    
    product = soup.find(id="productTitle").get_text().strip()
    
    try:
        price = soup.find(id = 'priceblock_ourprice').get_text()
    except Exception as e:
        price = soup.find(id = 'priceblock_dealprice').get_text()

    #print(price)
    return product,price



if __name__ == "__main__":
    app.secret_key = "secret"
    app.run(debug=True)