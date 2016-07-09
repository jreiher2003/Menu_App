import unittest 
from base import BaseTestCase 
from flask.ext.login import current_user
from app.models import User
from app import bcrypt

class TestUser(BaseTestCase):

    def test_user_registeration(self):
        with self.client:
            response1 = self.client.get("/signup", content_type="html/text")
            self.assert_template_used("signup.html")
            self.assertIn(b"Account Sign Up", response1.data)
            self.assertEqual(response1.status_code, 200)

            response = self.client.post("/signup", data=dict(
                username="Michael", email="michael@bulls.com",
                password="python", confirm="python", accept_tos="y"
            ), follow_redirects=True)
            self.assertIn(b"Thanks for registering", response.data)
            
            user = User.query.filter_by(email="michael@bulls.com").first()
            self.assertTrue(user.id == 2)
            self.assertTrue(user.username) == "Michael"

    def test_get_by_id(self):
        with self.client:
            self.client.post("/login", data=dict(
                email="jeffreiher@gmail.com", password="password"
            ), follow_redirects=True)
            self.assertTrue(current_user.is_active)
            self.assertTrue(current_user.id == 1)
            self.assertFalse(current_user.id == 20)

    def test_check_password(self):
        user = User.query.filter_by(email="jeffreiher@gmail.com").first()
        self.assertTrue(bcrypt.check_password_hash(user.password, "password"))
        self.assertFalse(bcrypt.check_password_hash(user.password, "foobar"))

    def test_login_logout(self):
        with self.client:
            self.client.get("/login", content_type="html/text")
            assert "Sign In"
            self.assert_template_used("login.html")
            self.client.post("/login", data=dict(
                email="jeffreiher@gmail.com",
                password="password"), follow_redirects=True)
            assert "You have signed in successfully!"
            self.client.get("/logout", follow_redirects=True)
            assert "You just logged out"
     
    def test_login_invalid(self):
        with self.client:
            self.client.post("/login", data=dict(
                email="fsssdfs",
                password="dsfsfs"), follow_redirects=True)
            assert "<strong>Invalid Credentials.</strong> Please try again." 
            self.assert_template_used("login.html")      


    
if __name__ == "__main__":
    unittest.main()