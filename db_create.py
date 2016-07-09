from app import app,db
# from app import db, user_datastore 
from app.models import Place, Menu, User#, Role, UserRoles
#from flask.ext.security.utils import encrypt_password

def create_users():
    user = User(
        username="j3ff_",
        email="jeffreiher@gmail.com",
        password="password",
        avatar="https://avatars0.githubusercontent.com/u/5870557?v=3&amp;s=460"
        )
    # role = Role(name="Admin", description="Super User of site")
    # userroles = UserRoles(user_id=1,role_id=1)
    db.session.add(user)
    # db.session.add(role)
    # db.session.add(userroles)
    
    db.session.commit()



def create_places():
    place1 = Place(name='Coffee Cafe', address="123 Cafe St.", city="Englewood", state="Florida", zip_="34225", website="http://cafe.com", phone="(941)585-3099", owner="Jeff Reiher", yrs_open=1)
    db.session.add(place1)
    place2 = Place(name='Jamacian Me Crazy', address="321 Smoking Blvd", city="Englewood", state="Florida", zip_="34225", website="http://smokeup.com", phone="(941) 585-3099", owner="Bumba Clod", yrs_open=14)
    db.session.add(place2)
    place3 = Place(name='Wack Arnolds', address="2020 Wackoff Ave", city="Englewood", state="Florida", zip_="34225", website="http://www.wackarnolds.com", phone="(941)585-3099", owner="Arnold Jackson", yrs_open=7)
    db.session.add(place3)
    place4 = Place(name='Jack n Crack', address="54098 Mission Rd", city="Englewood", state="Florida", zip_="34225", website="http://www.jackcrack.com", phone="(941)585-3099", owner="Jack MeOff", yrs_open=6)
    db.session.add(place4)
    place5 = Place(name='Egg Morning', address="8am Morning St.", city="Englewood", state="Florida", zip_="34225", website="http://www.eggmorning.com", phone="(941)585-3099", owner="Mona Eggstyle", yrs_open=1)
    db.session.add(place5)
    db.session.commit()
    print "just created the restaurant table."


    ############ PLACE1 MENU ITEMS ##################################################
    #################################################################################
    menuItem1 = Menu(name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$7.50", course = "Entree", place_id = place1.id)
    db.session.add(menuItem1)
    menuItem2 = Menu(name = "French Fries", description = "with garlic and parmesan", price = "$2.99", course = "Appetizer", place_id = place1.id)
    db.session.add(menuItem2)
    menuItem3 = Menu(name = "Chocolate Cake", description = "fresh baked and served with ice cream", price = "$3.99", course = "Dessert", place_id= place1.id)
    db.session.add(menuItem3)
    menuItem4 = Menu(name = "Sirloin Burger", description = "Made with grade A beef", price = "$7.99", course = "Entree", place_id= place1.id)
    db.session.add(menuItem4)
    menuItem5 = Menu(name = "Root Beer", description = "16oz of refreshing goodness", price = "$1.99", course = "Beverage", place_id= place1.id)
    db.session.add(menuItem5)
    print "place 1"
    ############ PLACE2 MENU ITEMS ##################################################
    #################################################################################
    menuItem6 = Menu(name = "Iced Tea", description = "with Lemon", price = "$.99", course = "Beverage", place_id = place2.id)
    db.session.add(menuItem6)
    menuItem7 = Menu(name = "Grilled Cheese Sandwich", description = "On texas toast with American Cheese", price = "$3.49", course = "Entree", place_id = place2.id)
    db.session.add(menuItem7)
    menuItem8 = Menu(name = "Chicken Stir Fry", description = "With your choice of noodles vegetables and sauces", price = "$7.99", course = "Entree", place_id = place2.id)
    db.session.add(menuItem8)
    menuItem9 = Menu(name = "Peking Duck", description = " A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", price = "$25", course = "Entree", place_id = place2.id)
    db.session.add(menuItem9)
    menuItem10 = Menu(name = "Spicy Tuna Roll", description = "Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ", price = "15", course = "Entree", place_id = place2.id)
    db.session.add(menuItem10)
    print "place 2"

    
    ############ PLACE3 MENU ITEMS ##################################################
    #################################################################################
    menuItem11 = Menu(name = "Nepali Momo ", description = "Steamed dumplings made with vegetables, spices and meat. ", price = "12", course = "Entree", place_id = place3.id)
    db.session.add(menuItem11)
    menuItem12 = Menu(name = "Beef Noodle Soup", description = "A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.", price = "14", course = "Entree", place_id = place3.id)
    db.session.add(menuItem12)
    menuItem13 = Menu(name = "Ramen", description = "a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.", price = "12", course = "Entree", place_id = place3.id)
    db.session.add(menuItem13)
    menuItem14 = Menu(name = "Pho", description = "a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", price = "$8.99", course = "Entree", place_id = place3.id)
    db.session.add(menuItem14)

    menuItem15 = Menu(name = "Chinese Dumplings", description = "a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.", price = "$6.99", course = "Appetizer", place_id = place3.id)
    db.session.add(menuItem15)
    print "place 3"
    ############ PLACE4 MENU ITEMS ##################################################
    #################################################################################
    menuItem16 = Menu(name = "Gyoza", description = "The most prominent differences between Japanese-style gyoza and Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt and soy sauce, and the fact that gyoza wrappers are much thinner", price = "$9.95", course = "Entree", place_id = place4.id)
    db.session.add(menuItem16)
    menuItem17 = Menu(name = "Stinky Tofu", description = "Taiwanese dish, deep fried fermented tofu served with pickled cabbage.", price = "$6.99", course = "Entree", place_id = place4.id)
    db.session.add(menuItem17)
    menuItem18 = Menu(name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$9.50", course = "Entree", place_id = place4.id)
    db.session.add(menuItem18)
    menuItem19 = Menu(name = "Cheese Burger", description = "Juicy grilled patty with tomato mayo and lettuce", price = "$7.50", course = "Entree", place_id = place4.id)
    db.session.add(menuItem19)
    menuItem20 = Menu(name = "French Fries", description = "with garlic and parmesan", price = "$2.99", course = "Appetizer", place_id = place4.id)
    db.session.add(menuItem20)
    print "place 4"
    ############ PLACE5 MENU ITEMS ##################################################
    #################################################################################
    menuItem21 = Menu(name = "Sirloin Burger", description = "Made with grade A beef", price = "$7.99", course = "Entree", place_id= place5.id)
    db.session.add(menuItem21)
    menuItem22 = Menu(name = "Grilled Cheese Sandwich", description = "On texas toast with American Cheese", price = "$3.49", course = "Entree", place_id = place5.id)
    db.session.add(menuItem22)
    menuItem23 = Menu(name = "Spicy Tuna Roll", description = "Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ", price = "15", course = "Entree", place_id = place5.id)
    db.session.add(menuItem23)
    menuItem24 = Menu(name = "Ramen", description = "a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.", price = "12", course = "Entree", place_id = place5.id)
    db.session.add(menuItem24)
    menuItem25 = Menu(name = "Stinky Tofu", description = "Taiwanese dish, deep fried fermented tofu served with pickled cabbage.", price = "$6.99", course = "Entree", place_id = place5.id)
    db.session.add(menuItem25)
    print "place 5"


    db.session.commit()
    print "just created menu items for each restaurant."



if __name__ == '__main__':
    db.drop_all()
    print "Just Dropped all tables"
    db.create_all()
    create_users()
    print "users created"
    create_places()
