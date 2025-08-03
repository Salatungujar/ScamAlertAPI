from flask import Blueprint, request, jsonify
from models import db, Blog
from flask_jwt_extended import jwt_required, get_jwt_identity,JWTManager,verify_jwt_in_request

blog_bp = Blueprint('blog', __name__)

# jwt = JWTManager(blog_bp)

# @jwt.unauthorized_loader
# def unauthorized_callback(callback):
#     print(">>> Missing or invalid JWT")
#     return jsonify({"msg": "Missing or invalid JWT"}), 401

# @jwt.invalid_token_loader
# def invalid_token_callback(reason):
#     print(">>> Invalid token:", reason)
#     return jsonify({"msg": "Invalid token"}), 422

@blog_bp.route('/blogs', methods=['POST'])
@jwt_required()
def create_blog():
    verify_jwt_in_request()
    uid = get_jwt_identity()
    print( get_jwt_identity(),">>>>>>>>>>>>>>>>>>>>>")
    data = request.get_json()
    blog = Blog(
        title=data['title'],
        content=data['content'],
        youtube_url=data.get('youtube_url'),
        author_id=get_jwt_identity()
    )
    db.session.add(blog)
    db.session.commit()
    return jsonify({"message": "Blog created"}), 201

@blog_bp.route('/blogs', methods=['GET'])
def get_blogs():
    blogs = Blog.query.order_by(Blog.created_at.desc()).all()
    return jsonify([
        {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "youtube_url": blog.youtube_url,
            "created_at": blog.created_at.isoformat()
        } for blog in blogs
    ])
