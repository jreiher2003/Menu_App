from flask_testing import TestCase
from app import app, db, bcrypt
from app.models import Place, Menu, Users



class BaseTestCase(TestCase):
    """A base test case."""
 
    def create_app(self):
        app.config.from_object('config.TestConfig')
        app.test_client()
        return app

    def setUp(self):
        db.create_all()
        db.session.add(Place(name='Testname',
                             address="123 Test st.",
                             city="Englewood",
                             state="Florida",
                             zip_="34224",
                             website="http://fake.com",
                             phone="123-456-7899",
                             owner="Jeff Reiher",
                             yrs_open=1))

        db.session.add(Menu(name="burger",
                            course="dinner",
                            description="test description",
                            price="$1.00",
                            place_id=1))
        
        db.session.add(Users(username="Jeffrey",
                            email="jeffreiher@gmail.com",
                            password=bcrypt.generate_password_hash("password"),
                            avatar="picofjeff.jpg"))

        
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
