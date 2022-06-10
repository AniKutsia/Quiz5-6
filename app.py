from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy


# http://quiz5.pythonanywhere.com/

# App Config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'quiz'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///my_db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# User Class

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), nullable=False)
    mail = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(500), nullable=False)


user = Users.query.first()

# News Class

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    info = db.Column(db.String(500), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(2000), nullable=False)


# Pages

# News

url_news = "https://myanimelist.net/news"
r_news = requests.get(url_news)
soup_news = BeautifulSoup(r_news.text, 'html.parser')
news_list = soup_news.find('div', {'class': 'news-list'})
l_news = news_list.find_all('div', {'class': 'news-unit clearfix rect'})


@app.route('/news')
def news():
    news_ = []

    for each in l_news:
        title = each.find('p', {'class': 'title'}).text
        text = each.find('div', {'class': 'text'}).text
        author = each.find('p', {'class': 'info di-ib'}).a.text
        image_url = each.find('img').attrs['src']
        tag_list = each.find_all('a', {'class': 'tag'})
        tags = []
        for t in tag_list:
            tags.append(t.text)
        a_news = {'title': title, 'text': text, 'author': author, 'image_url': image_url, 'tags': tags}
        news_.append(a_news)

    return render_template('news.html', news=news_)


# Home

@app.route('/')
def home():
    news_ = []

    for each in l_news:
        title = each.find('p', {'class': 'title'}).text
        text = each.find('div', {'class': 'text'}).text
        author = each.find('p', {'class': 'info di-ib'}).a.text
        image_url = each.find('img').attrs['src']
        tag_list = each.find_all('a', {'class': 'tag'})
        tags = []
        for t in tag_list:
            tags.append(t.text)
        a_news = {'title': title, 'text': text, 'author': author, 'image_url': image_url, 'tags': tags}
        if len(news_) < 4:
            news_.append(a_news)

    return render_template('index.html', news=news_)


# Top Anime

url = 'https://myanimelist.net/topanime.php'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
table = soup.find('table', {'class': 'top-ranking-table'})
anime_list_table = table.find_all('tr', {'class': 'ranking-list'})


@app.route('/top_anime')
def top_anime():
    anime_list = []

    for each in anime_list_table:
        rank = each.find('span', {'class': 'top-anime-rank-text'}).text
        title = each.h3.a.text
        info = each.find('div', {'class': 'information di-ib mt4'}).text
        score = each.find('span', {'class': 'score-label'}).text
        url = each.img.attrs['data-src']

        anime = {'rank': rank, 'title': title, 'info': info, 'score': score, 'url': url}
        anime_list.append(anime)

    return render_template('top_anime.html', anime_list=anime_list)


# Top Airing

url_airing = 'https://myanimelist.net/topanime.php?type=airing'
r_airing = requests.get(url_airing)
soup_airing = BeautifulSoup(r_airing.text, 'html.parser')
table_airing = soup_airing.find('table', {'class': 'top-ranking-table'})
airing_list_table = table_airing.find_all('tr', {'class': 'ranking-list'})


@app.route('/top_airing')
def top_airing():
    airing_list = []

    for each in airing_list_table:
        rank = each.find('span', {'class': 'top-anime-rank-text'}).text
        title = each.h3.a.text
        info = each.find('div', {'class': 'information di-ib mt4'}).text
        score = each.find('span', {'class': 'score-label'}).text
        url = each.img.attrs['data-src']

        anime = {'rank': rank, 'title': title, 'info': info, 'score': score, 'url': url}
        airing_list.append(anime)

    return render_template('top_airing.html', anime_list=airing_list)


# Most Popular

url_popular = 'https://myanimelist.net/topanime.php?type=bypopularity'
r_popular = requests.get(url_popular)
soup_popular = BeautifulSoup(r_popular.text, 'html.parser')
table_popular = soup_popular.find('table', {'class': 'top-ranking-table'})
most_popular_anime = table_popular.find_all('tr', {'class': 'ranking-list'})


@app.route('/most_popular')
def most_popular():
    popular_anime = []

    for each in most_popular_anime:
        rank = each.find('span', {'class': 'top-anime-rank-text'}).text
        title = each.h3.a.text
        info = each.find('div', {'class': 'information di-ib mt4'}).text
        score = each.find('span', {'class': 'score-label'}).text
        url = each.img.attrs['data-src']

        anime = {'rank': rank, 'title': title, 'info': info, 'score': score, 'url': url}
        popular_anime.append(anime)

    return render_template('most_popular.html', anime_list=popular_anime)


# Top Movies

url_movies = 'https://myanimelist.net/topanime.php?type=movie'
r_movies = requests.get(url_movies)
soup_movies = BeautifulSoup(r_movies.text, 'html.parser')
table_movies = soup_movies.find('table', {'class': 'top-ranking-table'})
movies_table = table_movies.find_all('tr', {'class': 'ranking-list'})


@app.route('/top_movies')
def top_movies():
    movies = []

    for each in movies_table:
        rank = each.find('span', {'class': 'top-anime-rank-text'}).text
        title = each.h3.a.text
        info = each.find('div', {'class': 'information di-ib mt4'}).text
        score = each.find('span', {'class': 'score-label'}).text
        url = each.img.attrs['data-src']

        anime = {'rank': rank, 'title': title, 'info': info, 'score': score, 'url': url}
        movies.append(anime)

    return render_template('top_movies.html', anime_list=movies)


# LogIn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']

        currentUser = Users.query.filter_by(mail=mail).first()
        if currentUser is not None:
            if currentUser.password == password:
                session['mail'] = mail
                session['username'] = currentUser.username
                return redirect(url_for('profile'))
            else:
                flash('პაროლი არასწორია')
        else:
            flash('აქაუნთი ვერ მოიძებნა')

    return render_template('login.html')


#

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        mail = request.form['mail']
        password = request.form['password']
        checkMail = Users.query.filter_by(mail=mail).first()
        if checkMail is None:
            user = Users(username=username, mail=mail, password=password)
            db.session.add(user)
            db.session.commit()
            session['mail'] = mail
            session['username'] = user.username
            return redirect(url_for('profile'))
        else:
            flash('აქაუნთი ასეთი ელ ფოსტით უკვე რეგისტრირებულია')
    return render_template('registration.html')


# LogOut

@app.route('/logout')
def logout():
    session.pop('mail', None)
    session.pop('username', None)
    return redirect(url_for('login'))


# Profile

@app.route('/profile')
def profile():
    return render_template('profile.html')


# Run

if __name__ == '__main__':
    app.run(debug=True)
