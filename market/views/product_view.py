from datetime import datetime  # 날짜 기능을 쓰기 위해 추가
from flask import Blueprint, render_template, request, url_for, redirect # request 추가
from market import db  # db.session을 쓰기 위해 추가
from market.models import Item, Comment  # Comment 모델 추가 (4개코드 오늘 수정함 4월14일)

bp = Blueprint('items', __name__, url_prefix='/items')

# 글쓰기
@bp.route('/product-upload/')
def product_upload():
    return render_template('items/write.html')

# 상품 상세페이지
@bp.route('/product-details/<int:item_id>/')   # 1. 주소 뒤에 상품 ID를 받도록 설정합니다.
def product_details(item_id):
    # 2. DB에서 ID에 해당하는 상품 정보를 하나 가져옵니다.
    product = Item.query.get_or_404(item_id)

    print(product.item_price)

    # 3. [추가] DB에서 전체 상품 목록을 가져옵니다 (최신순 6개)
    # .limit(6)을 붙여서 딱 6개만 가져오게 조절할 수 있습니다.
    item_list = Item.query.order_by(Item.item_reg_datetime.desc()).limit(6).all()

    # [데이터 가공] 날짜 형식을 미리 문자로 바꿉니다.
    formatted_date = product.item_reg_datetime.strftime('%Y-%m-%d %H:%M')

    # 4. 가져온 데이터를 'product'라는 이름으로 HTML에 전달합니다.
    return render_template('items/PDP.html', product=product, formatted_date=formatted_date, item_list=item_list)

# 카테고리별 페이지
@bp.route('/product-categories/<int:category_id>/')
def product_categories(category_id):
    return render_template('items/CP.html', category_id = category_id)


# 1. @bp.route: 이 함수를 실행할 '인터넷 주소'를 정합니다.  (오늘 새로추가 4월14일)
# <int:item_id>는 "몇 번 상품에 댓글을 달 건지" 숫자를 받아오겠다는 뜻.
# methods=('POST',)는 사용자가 '제출' 버튼을 눌러 데이터를 보낼 때만 작동하라는 명령입니다.
@bp.route('/comment/create/<int:item_id>', methods=('POST',))
def comment_create(item_id):
    # 2. Item.query.get_or_404:
    # 받아온 아이디(item_id)로 DB에서 해당 상품을 찾습니다.
    # 만약 없는 상품이면 "페이지를 찾을 수 없음(404)" 에러를 띄워줍니다.
    item = Item.query.get_or_404(item_id)

    # 3. request.form.get('content'):
    # HTML의 <textarea name="content">에 사용자가 방금 입력한 글자들을 쏙 뽑아서 변수에 저장합니다.
    content = request.form.get('content')

    # 4. if content:
    # 댓글 내용이 비어있지 않을 때만 아래 작업을 시작합니다. (빈 댓글 방지)
    if content:
        # 5. Comment(...): 새로운 댓글 '객체'를 만듭니다.
        # content=내용, create_date=지금 시간, item=아까 찾은 그 상품!
        # 이렇게 연결해줘야 나중에 "아이폰 글에 달린 댓글"인 줄 알게 됩니다.
        comment = Comment(content=content, create_date=datetime.now(), item=item)

        # 6. db.session.add:
        # 만든 댓글을 DB에 넣기 전에 일단 '장바구니'에 담는 단계입니다.
        db.session.add(comment)

        # 7. db.session.commit:
        # "진짜로 저장해!"라고 명령하는 단계입니다. 이 코드가 실행되어야 하드디스크에 기록됩니다.
        db.session.commit()

    # 8. redirect:
    # 저장이 끝났으니 다시 상품 상세 페이지('main_view.detail')로 화면을 돌려보냅니다.
    # 그래야 사용자가 자기가 쓴 댓글이 바로 달린 걸 확인할 수 있겠죠?
    return redirect(url_for('items.product_details', item_id=item_id))

@bp.route('/user/items/<int:user_id>/')
def user_items(user_id):
    # DB에서 해당 유저가 올린 상품만 필터링해서 가져옴
    # (예: Item 모델에 user_id 필드가 있다고 가정)
    item_list = Item.query.filter_by(user_id=user_id).order_by(Item.item_reg_datetime.desc()).all()
    return render_template('main.html', item_list=item_list)