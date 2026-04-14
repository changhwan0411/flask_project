from flask import Blueprint, render_template, g
from market.views.auth_view import login_required
from market.models import Item, Favorite, Review

bp = Blueprint('mypage', __name__, url_prefix='/mypage')


@bp.route('/')
@login_required
def mypage():
    user = g.user

    products = Item.query.filter_by(user_id=user.id, is_deleted=False)\
        .order_by(Item.created_at.desc()).all()

    wishes = Favorite.query.filter_by(user_id=user.id)\
        .order_by(Favorite.created_at.desc()).all()

    reviews = Review.query.filter_by(target_user_id=user.id)\
        .order_by(Review.created_at.desc()).all()

    return render_template(
        'personal/mypage.html',
        user=user,
        products=products,
        wishes=wishes,
        reviews=reviews
    )