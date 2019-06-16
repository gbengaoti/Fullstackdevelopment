from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem
 
engine = create_engine('sqlite:///restaurantmenu.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            restaurant_rows = session.query(Restaurant).all()
            message = "" 
            message += "<html><body>"
            message += "<a href='/restaurants/new'>Make a new restaurant here</a><br><br>"
            for r in restaurant_rows:
                r_all = session.query(Restaurant).filter(Restaurant.name == r.name).all()
                link_edit = '/restaurants/'+ str(r_all[0].id) + '/edit'
                link_delete = '/restaurants/'+ str(r_all[0].id) + '/delete'
                message += "<p>" + r.name + "<br><a href=" + link_edit + ">Edit</a>" + "<br><a href=" + link_delete + ">Delete</a>"+ "</p>"
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return

        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "" 
            message += "<html><body>"
            message += "<h1>Make a new restaurant</h1>"
            message += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name='newRestaurantName' type='text' placeholder='create a new restaurant'><input type='submit' value='Create'>"
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return

        if self.path.endswith("/edit"):
            restaurantIDPath = self.path.split("/")[2]
            restaurantQuery = session.query(Restaurant).filter(Restaurant.id == restaurantIDPath).one()
            
            if restaurantQuery:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = "" 
                message += "<html><body>"
                message += "<h1>"
                message += restaurantQuery.name
                message +=  "</h1>"
                message += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                message += "<input name='updateRestaurantName' type='text' placeholder = '%s' >" % restaurantQuery.name 
                message += "<input type='submit' value='Update'>"
                message += "</form>"
                message += "</body></html>"
                self.wfile.write(message)
                print message
                return

        if self.path.endswith("/delete"):
            restaurantIDPath = self.path.split("/")[2]
            restaurantQuery = session.query(Restaurant).filter(Restaurant.id == restaurantIDPath).one()
            
            if restaurantQuery:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = "" 
                message += "<html><body>"
                message += "<h1>Are you sure you want to delete %s " % restaurantQuery.name+" ?</h1>"
                message += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/delete' >" % restaurantIDPath
                message += "<input type='submit' value='Delete'>"
                message += "</form>"
                message += "</body></html>"
                self.wfile.write(message)
                print message
                return


        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('updateRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    restaurantQuery = session.query(Restaurant).filter(Restaurant.id == restaurantIDPath).one()

                    # Create new Restaurant Object
                    if restaurantQuery != []:
                        restaurantQuery.name = messagecontent[0]
                        session.add(restaurantQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]

                restaurantQuery = session.query(Restaurant).filter(Restaurant.id == restaurantIDPath).one()

                # Create new Restaurant Object
                if restaurantQuery != []:
                    session.delete(restaurantQuery)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
               
        except:
            pass


def main():

    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()