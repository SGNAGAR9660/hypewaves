# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from config import get_db_connection
from flask_minify import Minify
import secrets
import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
Minify(app=app, html=True, js=True, cssless=True)

def fetch_articles_by_category(category):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles WHERE category=%s ORDER BY id DESC LIMIT 6', (category,))
    latest = cursor.fetchall()
    cursor.execute('SELECT * FROM articles WHERE category=%s ORDER BY id ASC LIMIT 6', (category,))
    old = cursor.fetchall()
    cursor.close()
    conn.close()
    return latest, old

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles ORDER BY id DESC LIMIT 6')
    latest_articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', latest_articles=latest_articles)

@app.route('/tech')
def tech():
    latest_articles, old_articles = fetch_articles_by_category('tech')
    return render_template('tech.html', latest_articles=latest_articles, old_articles=old_articles)

@app.route('/ai')
def ai():
    latest_articles, old_articles = fetch_articles_by_category('ai')
    return render_template('ai.html', latest_articles=latest_articles, old_articles=old_articles)

@app.route('/entertainment')
def entertainment():
    latest_articles, old_articles = fetch_articles_by_category('entertainment')
    return render_template('entertainment.html', latest_articles=latest_articles, old_articles=old_articles)

@app.route('/news')
def news():
    latest_articles, old_articles = fetch_articles_by_category('news')
    return render_template('news.html', latest_articles=latest_articles, old_articles=old_articles)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin@123':
            session['admin_logged_in'] = True
            flash('Login Successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('admin_login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    return render_template('dashboard.html')

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        image_url = request.form['image_url']
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO articles (title, content, category, image_url) VALUES (%s, %s, %s, %s)', (title, content, category, image_url))
            conn.commit()
            flash('Article added successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash('Error adding article.', 'danger')
            print(e)
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_article.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('admin_login'))

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles WHERE id = %s', (article_id,))
    article = cursor.fetchone()
    cursor.close()
    conn.close()
    if article:
        return render_template('article_detail.html', article=article)
    else:
        return render_template('404.html'), 404

@app.route('/all_articles')
def all_articles():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles ORDER BY id DESC')
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('all_articles.html', articles=articles)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(f"New Contact Message: {name}, {email}, {message}")
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/google9edf697d52ec1d5c.html')
def google_verification():
    return send_from_directory('static', 'google9edf697d52ec1d5c.html')

@app.route('/sitemap.xml')
def sitemap():
    pages = []
    ten_days_ago = (datetime.datetime.now() - datetime.timedelta(days=10)).date().isoformat()
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append(f"https://www.hypewaves.net{rule.rule}")
    sitemap_xml = render_template('sitemap_template.xml', pages=pages, lastmod=ten_days_ago)
    response = app.response_class(sitemap_xml, mimetype='application/xml')
    return response

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/ads.txt')
def ads_txt():
    return open('static/ads.txt').read(), 200, {'Content-Type': 'text/plain'}

@app.route('/search')
def search():
    query = request.args.get('q')
    if query:
        return render_template('search_results.html', query=query)
    else:
        flash('Please enter a search term.', 'warning')
        return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
