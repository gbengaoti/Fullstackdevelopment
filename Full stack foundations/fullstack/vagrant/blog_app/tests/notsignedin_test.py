# Test when user logged out
# Guest can only view articles
# Guest has access to all JSON APIs 
    ####Comments 
    # get comments from non existing article
    # get comments from article where no comments
    # get comments from article with comments
    ####Users
    # get all users when no users exist
    ###Articles
    # get articles when user has no article
    # get articles from non exisiting user
    ###Article
    # get non existing article from existing user
    # wrong user id, right article_id

import requests, random

base_uri = "http://localhost:8000/"

# test that guest can access the home page
query = "index"
uri =  base_uri + query
print("Sending query for:", uri)
try:
  r = requests.get(uri)
  if r.status_code != 200:
    print("The server returned status code {}"
          "instead of a 200 OK.".format(r.status_code))
  else:
    print("Test 1 PASSED - Guest user can access home page")
except requests.ConnectionError:
  print("Couldn't connect to the server. Is it running on port 8000?")
except requests.RequestException as e:
  print("Couldn't communicate with the server ({})".format(e))
  print("If it's running, take a look at the server's output.")