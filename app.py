from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.app_context().push()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/support/<string:theme>')
def post_support(theme):
    return render_template('support.html', theme=theme)

@app.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', article=article)

@app.route('/article/<int:id>/delete')
def article_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/articles')
    except:
        return "Error"

@app.route('/article/<int:id>/update', methods=['POST', 'GET'])
def article_update(id):
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.author = request.form['author']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect(f'/article/{id}')
        except:
            return "Error"
    else:
        return render_template('update_article.html', article=article)

@app.route('/create-article', methods=['POST', 'GET'])
def create_arcticle():
    if request.method == 'POST':
        _title = request.form['title']
        _author = request.form['author']
        _text = request.form['text']
        article = Article(title=_title, author=_author, text=_text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template('create_article.html')


if __name__ == '__main__':
    app.run(debug=True)
