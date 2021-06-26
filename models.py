
from app import db




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