import unittest 
from base import BaseTestCase 

class TestApi(BaseTestCase):

    def test_api(self):
        response = self.client.get("/api", content_type="html/text")
        self.assertTrue(response.status_code, 200)
        assert "this is api page"

    def test_restaurant_api(self):
        response = self.client.get("/restaurant/JSON/", content_type="application/json")
        self.assertTrue(response.status_code, 200)
        self.assertIn("Testname", response.data)

    def test_restaurant_menu_api(self):
        response = self.client.get("/restaurant/1/menu/JSON", content_type="application/json")
        self.assertTrue(response.status_code, 200)
        self.assertIn("burger", response.data)

    def test_single_menu_item(self):
        response = self.client.get("/restaurant/1/menu/1/JSON", content_type="application/json")
        self.assertTrue(response.status_code, 200)
        self.assertIn("burger", response.data)



if __name__ == "__main__":
    unittest.main()