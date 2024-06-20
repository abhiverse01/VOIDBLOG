from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)  # New field for image URL
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    posts = BlogPost.query.all()
    return render_template('home.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog.html', post=post)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']
        
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            image_url = url_for('static', filename=f'uploads/{image.filename}')
        else:
            image_url = None
        
        new_post = BlogPost(title=title, content=content, image_url=image_url)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('write.html')

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content, 'date_posted': post.date_posted} for post in posts])

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
