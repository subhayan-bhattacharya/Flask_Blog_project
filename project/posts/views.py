from flask import session,render_template,redirect,url_for,Blueprint,request,flash,jsonify
from project.models.posts_model import Post
from project.models.user_model import User
from project.models.comments_model import Comment
from project.models.tag_model import Tag
from project.users.decorators import login_required
from .form import PostForm
from wtforms import SelectField,SelectMultipleField
from slugify import slugify

posts_blueprint = Blueprint(
    'posts',
    __name__,
    template_folder='templates/posts'
)

def process_form(form,user,edit=False,create=False,post_id=None):
    edited = False
    title = form.title.data
    body = form.body.data
    slug = slugify(title)
    tags = form.tag.data
    author_id = user.id
    if post_id:
        new_post = Post.get_post_by_id(id=post_id)
        new_post.title = title
        new_post.body = body
    else:
        new_post = Post(title=title, body=body, slug=slug, author_id=author_id,is_live=True)
        
    if form.new_tag.data:
        if edit:
            new_post.tags = []
            edited = True
        new_tags = form.new_tag.data.split(',')
        #Create new tag object and then add it to the post table
        for new_tag in new_tags:
            new_tag_obj = Tag(name=new_tag)
            new_post.tags.append(new_tag_obj)
    for tagid in tags:
        if edit:
            if not edited:
                new_post.tags = []
        tag_obj = Tag.get_tag_by_id(id=tagid)
        new_post.tags.append(tag_obj)
    if create:
        print ("Is this going inside create portion")
        if new_post.save_to_db():
            user.is_author = True
            if user.save_to_db():
                session['is_author'] = True
                session['author_id'] = user.id
                flash("Post successfully created")
            else:
                flash("Could  not create post")
        else:
            flash("Could not create new post")
    else:
        print (new_post.id)
        print (new_post.title)
        print (new_post.body)
        new_post.save_edited_to_db()
        flash("Post successfully edited")
    

@posts_blueprint.route('/')
@posts_blueprint.route('/index')
@posts_blueprint.route('/index/<int:page>')
def index(page=1):
    posts = []
    print ("Going to page: {}".format(str(page)))
    added_posts = Post.get_all_posts(page)

    if not request.is_xhr:
        return render_template('index.html',posts=added_posts,user=User.get_current_user())
    else:
        # if request is coming from an ajax request
        response_full = {}
        
        data = []

        for post in added_posts.items:
            response_data = {}
            response_data['title'] = post.title
            response_data['author'] = post.user.username
            response_data['author_id'] = post.user.id
            response_data['date'] = post.date.strftime('%Y-%m-%d')
            response_data['link'] = "/get_post/" + post.slug
            data.append(response_data)
        response_full['data'] = data

        if added_posts.has_prev:
            response_full['has_prev'] = True
            response_full['prev_page_num'] = added_posts.prev_num
        else:
            response_full['has_prev'] = False
        if added_posts.has_next:
            response_full['has_next'] = True
            response_full['next_page_num'] = added_posts.next_num
        else:
            response_full['has_next'] = False
        print(response_full)
        return jsonify(response_full)



@posts_blueprint.route('/post',methods=['GET','POST'])
@login_required
def post():
    setattr(PostForm,"tag",SelectMultipleField('Tags', choices=Tag.get_all_tags()))
    form = PostForm()
    user = User.get_current_user()
    if form.validate_on_submit():
        process_form(form,user,edit=False,create=True)
        return redirect(url_for('posts.index'))
    return render_template('post.html',form=form,user=user,edit=False,heading="Add a new post")


@posts_blueprint.route('/get_post/<string:slug>')
@login_required
def get_post(slug):
    post_obj = Post.get_post_by_slug(slug)
    return render_template('post_details.html',post=post_obj,user=User.get_current_user())
    
    
@posts_blueprint.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post_obj = Post.get_post_by_id(id=post_id)
    if post_obj.author_id == session['author_id']:
        post_obj.is_live = False
        if post_obj.save_to_db():
            flash("Post deleted")
        else:
            flash("Could not delete post")
    else:
        flash("You are not allowed to delete this post")
    return redirect('/index')
    
    
@posts_blueprint.route('/edit_post/<int:post_id>',methods=['GET','POST'])
@login_required
def edit_post(post_id):
    post_obj = Post.get_post_by_id(id=post_id)
    setattr(PostForm,"tag",SelectMultipleField('Tags', choices=Tag.get_all_tags()))
    user = User.get_current_user()
    form = PostForm(obj=post_obj)
    if form.validate_on_submit():
        process_form(form,user,edit=True,create=False,post_id=post_id)
        return redirect(url_for('posts.index'))
    return render_template('post.html',form=form,user=user,edit=True,post_id=post_id,heading="Edit Post")
    
        
    
@posts_blueprint.route('/get_all_tag_posts/<string:tag_name>')
@posts_blueprint.route('/get_all_tag_posts/<string:tag_name>/<int:page>')
@login_required
def get_all_tag_posts(tag_name,page=1):
    all_posts = Post.get_all_tag_posts(tag_name,page)
    if not request.is_xhr:
        return render_template ('get_all_tag_posts.html',posts=all_posts,user=User.get_current_user(),tag=tag_name)
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