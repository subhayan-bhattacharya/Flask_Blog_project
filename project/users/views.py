from flask import session,render_template,redirect,url_for,Blueprint,request,flash,jsonify
from project.models.posts_model import Post
from project.models.user_model import User
from project.models.comments_model import Comment
from project.models.tag_model import Tag
from .form import LoginForm,RegisterForm
from .decorators import login_required
from werkzeug.security import generate_password_hash, check_password_hash

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates/users'
)

@users_blueprint.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == "GET" and request.args.get("next"):
        session['next'] = request.args.get("next", None)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='sha256')
        user = User.get_user_by_username(username=username)
        if user:
            returned_password = user.password
            if check_password_hash(returned_password, password):
                session['username'] = username
                if user.is_author:
                    print ("Checking inside login route")
                    session['is_author'] = True
                    session['author_id'] = user.id
                if 'next' in session:
                    next = session['next']
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('posts.index'))
        flash("Username or password is incorrect")
        return redirect(url_for('users.register'))
    return render_template('login.html',form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    if 'username' in session:
        session.pop('username')
    if 'is_author' in session:
        session.pop('is_author')
        session.pop('author_id')
    return redirect(url_for('posts.index'))

@users_blueprint.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        fullname = form.fullname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        existing_user = User.get_user_by_username(username=username)
        if not existing_user:
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(fullname=fullname,username=username, password=hashed_password,email=email,is_author=False)
            if new_user.save_to_db():
                session['username'] = username
                flash("User successfully registered")
                return redirect(url_for('posts.index'))
            else:
                flash("Could not create new user")
        else:
            flash("User already exists")
            return redirect(url_for('users.login'))
    return render_template('register.html',form=form)
    
    
@users_blueprint.route('/get_all_author_posts/<string:author_id>')
@users_blueprint.route('/get_all_author_posts/<string:author_id>/<int:page>')
@login_required
def get_all_author_posts(author_id,page=1):
    author = User.get_by_id(author_id)
    print ("trying to get post by :{} and page : {}".format(author_id,page))
    all_posts = Post.get_all_author_posts(author_id,page)
    if not request.is_xhr:
        return render_template('get_all_author_posts.html',posts=all_posts,author_id=author_id,user=User.get_current_user(),authorname=author.username)
    else:
        response_full = {}
        
        data = []

        for post in all_posts.items:
            response_data = {}
            response_data['title'] = post.title
            response_data['author'] = post.user.username
            response_data['author_id'] = post.user.id
            response_data['date'] = post.date.strftime('%Y-%m-%d')
            response_data['link'] = "/get_post/" + post.slug
            data.append(response_data)
        response_full['data'] = data

        if all_posts.has_prev:
            response_full['has_prev'] = True
            response_full['prev_page_num'] = all_posts.prev_num
        else:
            response_full['has_prev'] = False
        if all_posts.has_next:
            response_full['has_next'] = True
            response_full['next_page_num'] = all_posts.next_num
        else:
            response_full['has_next'] = False
        print(response_full)
        return jsonify(response_full)

