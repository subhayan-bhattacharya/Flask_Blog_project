from flask import session,render_template,redirect,url_for,Blueprint,request,flash,jsonify
from project.models.comments_model import Comment
from project.models.user_model import User
from project.users.decorators import login_required


comments_blueprint = Blueprint(
    'comments',
    __name__,
    template_folder='templates/comments'
)

@comments_blueprint.route('/get_all_comments/<int:post_id>/<int:page>/')
def get_all_comments(post_id,page):
    if request.is_xhr:
        comments_json = {}
        all_comments = Comment.get_all_comments(post_id,page)
        print (all_comments.items)
        if len(all_comments.items) == 0:
            comments_json['comments_returned'] = 0
        else:
            data = []
            for comment in all_comments.items:
                comments_data = {}
                author_id = comment.commenter_id
                author = User.get_by_id(id=author_id)
                comments_data['name'] = author.username
                comments_data['comment'] = comment.comment
                comments_data['date'] = comment.date.strftime('%Y-%m-%d')
                data.append(comments_data)
            comments_json['data'] = data
            
            if all_comments.has_prev:
                comments_json['has_prev'] = True
                comments_json['prev_page_num'] = all_comments.prev_num
            else:
                comments_json['has_prev'] = False
            if all_comments.has_next:
                comments_json['has_next'] = True
                comments_json['next_page_num'] = all_comments.next_num
            else:
                comments_json['has_next'] = False
        comments_json['comments_returned'] = len(all_comments.items)    
            
        print (comments_json)
                
        return jsonify(comments_json)

@comments_blueprint.route('/post_comments',methods=['POST'])
def post_comments():
    if request.is_xhr:
        data = request.json
        comment_obj = Comment(commenter_id=data['user_id'],post_id=data['post_id'],comment=data['comment_str'])
        if not comment_obj.save_to_db():
            flash("Could not save comment to db")
            return jsonify({"message":"failed"})
        else:
            return jsonify({"message":"success"})
            


