# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
# from flask_login import login_user, login_required, logout_user, current_user

from src import app, db
from src.models import News, forge, initdb


@app.route('/', methods=['GET', 'POST'])
def index():
    # initdb(True)
    # forge()
    news_list = News.query.all()
    # print(news)
    return render_template('index.html', news_list=news_list)


@app.route("/refresh/", methods=['POST'])
def refresh():

    initdb(True)
    forge() 

    return redirect(url_for('index'))


# @app.route('/movie/delete/<int:movie_id>', methods=['POST'])
# @login_required
# def delete(movie_id):
#     movie = Movie.query.get_or_404(movie_id)
#     db.session.delete(movie)
#     db.session.commit()
#     flash('Item deleted.')
#     return redirect(url_for('index'))


# @app.route('/settings', methods=['GET', 'POST'])
# @login_required
# def settings():
#     if request.method == 'POST':
#         name = request.form['name']

#         if not name or len(name) > 20:
#             flash('Invalid input.')
#             return redirect(url_for('settings'))

#         user = User.query.first()
#         user.name = name
#         db.session.commit()
#         flash('Settings updated.')
#         return redirect(url_for('index'))

#     return render_template('settings.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         if not username or not password:
#             flash('Invalid input.')
#             return redirect(url_for('login'))

#         user = User.query.first()

#         if username == user.username and user.validate_password(password):
#             login_user(user)
#             flash('Login success.')
#             return redirect(url_for('index'))

#         flash('Invalid username or password.')
#         return redirect(url_for('login'))

#     return render_template('login.html')


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('Goodbye.')
#     return redirect(url_for('index'))