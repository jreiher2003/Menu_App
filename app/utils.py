from app import app, db 
from app.models import Users

def create_user(login_session):
    new_user = Users(username=login_session['username'], email=login_session['email'], avatar=login_session['picture'])
    db.session.add(new_user)
    db.session.commit()
    user = Users.query.filter_by(email=login_session['email']).one()
    return user.id 

def get_user_info(user_id):
    user = Users.query.filter_by(id=user_id).one()
    return user 

def get_user_id(email):
    try:
        user = Users.query.filter_by(email=email).one()
        return user.id 
    except:
        return None 

