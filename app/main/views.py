from flask import render_template,request,url_for,redirect,abort
from . import main
from ..models import User,Blog,Post,Comment
from flask_login import login_required, current_user
from .forms import PostForm,BlogForm,CommentForm,UpdateProfile
from .. import db,photos
from ..request import get_random_quote
import  markdown2

@main.route('/')
def index():
    '''
    view root that returns the index page and its data
    '''
    blog = Blog.get_blogs()
    random_quote = get_random_quote()

    return render_template('index.html', blog = blog, random_quote = random_quote)

@main.route('/add/blog', methods=['GET','POST'])
@login_required
def new_blog():
    '''
    view new route that returns a page with a form to create a new blog
    '''
    form = BlogForm()

    if form.validate_on_submit():
        name = form.name.data
        new_blog = Blog(name=name)
        new_blog.save_blog()

        return redirect(url_for('.index'))

    title = 'New blog' 
    return render_template('new_blog.html', blog_form = form,title = title)

@main.route('/blogs/<int:id>')
@login_required
def blog(id):
    blog = Blog.query.get(id)    
    posts = Post.query.filter_by(blog=blog.id).all()

    return render_template('blog.html', posts=posts, blog=blog)

@main.route('/blogs/view_post/add/<int:id>', methods=['GET','POST'])
@login_required
def new_post(id):
    '''
    function to check posts form and fetch data from the fields
    '''
    form = PostForm()
    blog = Blog.query.filter_by(id=id).first()

    if blog is None:
        abort(404)

    if form.validate_on_submit():
        content = form.content.data
        new_post = Post(content=content,blog=blog.id,user_id=current_user.id)   
        new_post.save_post()
        return redirect(url_for('.blog',id=blog.id))

    title = 'New Post'
    return render_template('new_post.html', title = title, post_form = form, blog = blog)

@main.route('/blogs/view_post/<int:id>', methods =['GET', 'POST'])
@login_required
def view_post(id):
    '''
    function that returns a single post for comment to be added
    '''

    print(id)
    posts = Post.query.get(id)

    if posts is None:
        abort(404)

    comment = Comments.get_comments(id)
    return render_template('post.html', posts = posts, comment=comment, blog_id=id)

@main.route('/post/comment/new/<int:id>',methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentForm()
    Post = get_post(id)
    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data

        # updated comment instance
        new_comment = Comment(posts_id=Post.id,post_title=title,post_comment=comment,user=current_user)

        # save comment method
        new_comment.save_comment()
        return redirect(url_for('.post',id=post.id))
    
    title = f'{post.title} comment'
    return render_template('new_comment.html',title = title,comment_form=form,post=post)

@main.route('/comment/<int:id>')
def single_comment(id):
    comment=Comment.query.get(id)
    if comment is None:
        abort(404)
    format_comment = markdown2.markdown(comment.post,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('comment.html',comment=comment,format_comment=format_comment)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))