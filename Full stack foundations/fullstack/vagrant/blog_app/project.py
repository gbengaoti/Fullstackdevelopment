from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import User, Base, Article, Comments

engine = create_engine('sqlite:///blogarticles.db')
Base.metadata.bind = engine

session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

@app.before_request
def before_request():
    session()

@app.after_request
def close_session(response):
    session.remove()
    return(response)

user = {"name":"Gbenga"}

articles = [{"title":"Summer in Lodz", "article_body":"Summer is great in Lodz, ancient city though"}, {"title":"Summer in France", "article_body":"Summer is great in France, modern city though"}]


@app.route('/users/<int:user_id>')
def userArticles(user_id):
    #return "Page to show all articles for user"
    return render_template('user_articles.html', user = user, articles = articles)

@app.route('/users/<int:user_id>/<int:article_id>/view')
def viewUserArticle(user_id, article_id):
    #return "Page to show article %d for user %d" % (user_id, article_id)
    return render_template('view_article.html', user = user, article = articles[0])

@app.route('/user/<int:user_id>/article/new')
def addArticle(user_id):
    #return "Page to add new article for user"
    return render_template('add_article.html', user = user)

@app.route('/user/<int:user_id>/article/<int:article_id>/edit')
def editArticle(user_id, article_id):
    #return "Page to add edit article for user"
    return render_template('edit_article.html', user = user, article = articles[0])

@app.route('/user/<int:user_id>/article/<int:article_id>/delete')
def deleteArticle(user_id, article_id):
    #return "Page to add delete article for user"
    return render_template('delete_article.html', user = user, article = articles[0])

if __name__ == '__main__':
    app.debug = False
    app.run(host = '0.0.0.0', port = 5000)