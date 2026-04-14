from flask import Blueprint, render_template
from market.models import Item

bp = Blueprint('items', __name__, url_prefix='/items')

# 글쓰기
@bp.route('/product-upload/')
def product_upload():
    return render_template('items/write.html')

# 상품 상세페이지
@bp.route('/product-details/<int:item_id>/')
def product_details(item_id):
    product = Item.query.get_or_404(item_id)
    return render_template('items/PDP.html', product=product)

# 카테고리별 페이지
@bp.route('/product-categories/<int:category_id>')
def product_categories(category_id):
    return render_template('items/CP.html', category_id=category_id)