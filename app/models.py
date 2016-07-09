import datetime # pragma: no cover
from app import db, bcrypt # pragma: no cover
from slugify import slugify # pragma: no cover


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime(),  default=datetime.datetime.now())

    def __init__(self, username, email, password, avatar):
        self.username = username
        self.email = email 
        self.password = bcrypt.generate_password_hash(password)
        self.avatar = avatar

    def __repr__(self):
        return "<username-{}".format(self.username)

    @property 
    def serialize(self):
        return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "created_at": self.created_at
        }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    

class Place(db.Model):

    __tablename__ = 'place' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(250))
    city = db.Column(db.String(80))
    state = db.Column(db.String(20))
    zip_ = db.Column(db.String(10))
    website = db.Column(db.String)
    phone = db.Column(db.String)
    owner = db.Column(db.String)
    yrs_open = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    users = db.relationship("User")
    last_edit = db.Column(db.Integer)
    


    @property 
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "address" : self.address,
            "city" : self.city,
            "state" : self.state,
            "zip_" : self.zip_,
            "website" : self.website,
            "phone" : self.phone,
            "owner" : self.owner,
            "yrs_open" : self.yrs_open
        } 

    @property 
    def name_slug(self):
        return slugify(self.name)

    def __repr__(self):
        return '<Place %r>' % (self.name)


class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    course = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.String(8))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    place = db.relationship(Place)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    users = db.relationship("User")
    last_edit = db.Column(db.Integer)
    

    @property 
    def name_slug(self):
        return slugify(self.name)

    @property 
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "course" : self.course,
            "description" : self.description,
            "price" : self.price
        } 

    def __repr__(self):
        return '<MenuItem %r>' % (self.name)