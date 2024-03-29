from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from requests_oauthlib import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

app = Flask(__name__)
import google_auth
app.register_blueprint(google_auth.app)
from flask import session as login_session
import random
import string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import User, Base, Article, Comments

engine = create_engine('sqlite:///blogarticles.db')
Base.metadata.bind = engine

session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

#validate token
#check if user is logged in

@app.before_request
def before_request():
    session()

@app.after_request
def close_session(response):
    session.remove()
    return(response)

@app.route('/users/JSON')
def usersJSON():
    # get all users
    users = session.query(User).all()
    return jsonify(Users=[user.serialize for user in users])

@app.route('/')
@app.route('/signin')
def signinBlog():
    if google_auth.is_signed_in():
        return redirect(url_for('users'))
    else:
        # state = ''.join(random.choice(string.ascii_uppercase + string.digits)
        #                 for x in xrange(32))
        # login_session['state'] = state
        return render_template('signin.html', signed_in=google_auth.is_signed_in())  


@app.route('/signout')
def signoutBlog():
    if google_auth.is_signed_in():
        return redirect(url_for('google_auth.clear_credentials'))

@app.route('/users')
def users():
    users = session.query(User).all()
    return render_template('users.html', users = users)  

@app.route('/user/<int:user_id>/article/<int:article_id>/comments/JSON')
def commentsJSON(user_id, article_id):
    allComments = session.query(Comments).filter_by(article_id = article_id).all()
    return jsonify(Comments=[c.serialize for c in allComments])

@app.route('/user/<int:user_id>/articles/JSON')
def articlesJSON(user_id):
    articles = session.query(Article).filter_by(user_id = user_id).all()
    return jsonify(Articles= [article.serialize for article in articles])    

@app.route('/user/<int:user_id>/article/<int:article_id>/JSON')
def articleJSON(user_id, article_id):
    article = session.query(Article).filter_by(id = article_id, user_id = user_id).one()
    return jsonify(Article= article.serialize)    


@app.route('/users/<int:user_id>')
def userArticles(user_id):
    # search for user by ID
    user = session.query(User).filter_by(id = user_id).one()
    # get all articles with user ID
    articles = session.query(Article).filter_by(user_id = user_id).all()
    return render_template('user_articles.html', user = user, articles = articles, signed_in=google_auth.is_signed_in())

@app.route('/user/<int:user_id>/article/<int:article_id>/view', methods=['GET','POST'])
def viewUserArticle(user_id, article_id):
    # search article by user_id and article_id
    user = session.query(User).filter_by(id = user_id).one()
    article = session.query(Article).filter_by(id = article_id, user_id = user_id).one()
    allComments = session.query(Comments).filter_by(article_id = article_id).all()
    if request.method == 'POST':
        newComment = Comments(comment_text = request.form['comment'], article_id = article.id )
        session.add(newComment)
        session.commit()
        return redirect(url_for('viewUserArticle', user_id = user.id, article_id = article.id ))
    else:
        return render_template('view_article.html', user = user, article = article, comments = allComments, num_comments = len(allComments), signed_in=google_auth.is_signed_in())

@app.route('/user/<int:user_id>/article/new' , methods=['GET','POST'])
def addArticle(user_id):
    if google_auth.is_signed_in():
        user = session.query(User).filter_by(id = user_id).one()
        if request.method == 'POST':
            newArticle = Article(title = request.form['title'], article_body =request.form['body'], user_id = user_id)
            session.add(newArticle)
            session.commit()
            flash("New Post Added Successfully!")
            return redirect(url_for('userArticles', user_id = user_id))
        else:
            return render_template('add_article.html', user = user)
    else:
        flash("You need to be logged in to add an article")
        return redirect(url_for('userArticles', user_id = user_id))

@app.route('/user/<int:user_id>/article/<int:article_id>/edit' , methods=['GET','POST'])
def editArticle(user_id, article_id):
    if google_auth.is_signed_in():
        # get article from database
        user = session.query(User).filter_by(id = user_id).one()
        toEditArticle = session.query(Article).filter_by(id = article_id, user_id = user_id).one()
        if request.method == 'POST':
            if request.form['title']:
                toEditArticle.title = request.form['title']
            if request.form['body']:
                toEditArticle.article_body = request.form['body']
            session.add(toEditArticle)
            session.commit()
            flash("Post Successfully Updated !")
            return redirect(url_for('viewUserArticle', user_id = user_id, article_id = article_id))
        else:
            return render_template('edit_article.html', user = user, article = toEditArticle)
    else:
        flash("You need to be logged in to edit an article")
        return redirect(url_for('userArticles', user_id = user_id))

@app.route('/user/<int:user_id>/article/<int:article_id>/delete'  , methods=['GET','POST'])
def deleteArticle(user_id, article_id):
    # get article
    if google_auth.is_signed_in():
        user = session.query(User).filter_by(id = user_id).one()
        toDeleteArticle = session.query(Article).filter_by(id = article_id, user_id = user_id).one()
        if request.method == 'POST':
            session.delete(toDeleteArticle)
            session.commit()
            flash("Post Successfully Deleted")
            return redirect(url_for('userArticles', user_id = user_id))
        else:
            return render_template('delete_article.html', user = user, article = toDeleteArticle)
    else:
        flash("You need to be logged in to delete an article")
        return redirect(url_for('userArticles', user_id = user_id))

if __name__ == '__main__':
    app.secret_key = 'super_secret_blog_keys'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)