from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "M1WI1DV1GA22P2QX3EGN1COV3U1CNSJF0VYHUQJQM5Q5UGOA"
foursquare_client_secret = "5HJ0BDZ5EGZ4RLRTLER3BLMC5XXZFY5VNDF311UBIZK2BPBP"


def findARestaurant(mealType,location):
    restaurant_info = {}
    #1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    latitude, longitude = getGeocodeLocation(location)
    
    #2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s'% (foursquare_client_id, foursquare_client_secret, latitude, longitude, mealType))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    
    #3. Grab the first restaurant
    if result['response']['venues']:
        first_restaurant = result['response']['venues'][0]
        restaurant_info['name'] = first_restaurant['name']
        restaurant_address = first_restaurant['location']['formattedAddress']
        address = ""
        for i in restaurant_address:
            address += i + " "
        restaurant_address = address
        restaurant_info['address'] = restaurant_address
        venue_id = first_restaurant['id']

        #4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((venue_id,foursquare_client_id,foursquare_client_secret)))
        result = json.loads(h.request(url, 'GET')[1])
        #5. Grab the first image
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix
        else:
            #6. If no image is available, insert default a image url
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"
        #7. Return a dictionary containing the restaurant name, address, and image url 
        restaurant_info['image'] = imageURL
        return restaurant_info
    else:
        print "No Restaurants Found for %s" % location
        return "No Restaurants Found"
if __name__ == '__main__':
    print(findARestaurant("Pizza", "Tokyo, Japan"))
    # findARestaurant("Tacos", "Jakarta, Indonesia")
    # findARestaurant("Tapas", "Maputo, Mozambique")
    # findARestaurant("Falafel", "Cairo, Egypt")
    # findARestaurant("Spaghetti", "New Delhi, India")
    # findARestaurant("Cappuccino", "Geneva, Switzerland")
    # findARestaurant("Sushi", "Los Angeles, California")
    # findARestaurant("Steak", "La Paz, Bolivia")
    # findARestaurant("Gyros", "Sydney, Australia")