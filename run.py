from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock data for demonstration purposes
posts = {
    1: {
        'id': 1,
        'title': 'First Blog Post',
        'date_posted': '2023-01-01',
        'author': 'Author Name',
        'content': 'This is the content of the first blog post.',
        'categories': ['Category1', 'Category2'],
        'tags': ['Tag1', 'Tag2'],
        'comments': []
    }
}

@app.route('/')
def home():
    return render_template('home.html', posts=posts.values())

@app.route('/post/<int:post_id>')
def post(post_id):
    post = posts.get(post_id)
    if post:
        previous_post = next_post = None
        post_ids = list(posts.keys())
        current_index = post_ids.index(post_id)
        if current_index > 0:
            previous_post = posts[post_ids[current_index - 1]]
        if current_index < len(post_ids) - 1:
            next_post = posts[post_ids[current_index + 1]]
        return render_template('blog.html', post=post, previous_post=previous_post, next_post=next_post, related_posts=[p for p in posts.values() if p['id'] != post_id])
    return "Post not found", 404

@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    post = posts.get(post_id)
    if post:
        content = request.form.get('content')
        if content:
            post['comments'].append({'author': 'Anonymous', 'content': content})
        return redirect(url_for('post', post_id=post_id))
    return "Post not found", 404

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if post_id in posts:
        del posts[post_id]
        return redirect(url_for('home'))
    return "Post not found", 404

if __name__ == '__main__':
    app.run(debug=True)
