from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os

from sqlalchemy import MetaData

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}

# Extension 객체 생성

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))     # ORM 도구
migrate = Migrate()   # 테이블 구조 변경(DB migration) 관리

# Seed 데이터 (초기 데이터)

def init_item_status():
    """
    상품 상태 기본값 생성
    앱 최초 실행 시 DB에 자동 삽입됨
    """
    # from .models import Item_Status

    # 이미 데이터 있으면 생성 안함 (중복 방지)
    # if not ItemStatus.query.first():
    #     db.session.add_all([
    #         ItemStatus(item_status='판매중'),
    #         ItemStatus(item_status='예약중'),
    #         ItemStatus(item_status='판매완료'),
    #     ])
    #     db.session.commit()

def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.dirname(__file__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'market.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Extension 초기화
    
    db.init_app(app)
    migrate.init_app(app, db)



    SECRET_KEY = 'dev'
    app.config['SECRET_KEY'] = SECRET_KEY

    # 모델 등록
    from . import models


    # DB 생성 + Seed 데이터
    with app.app_context():
        db.create_all()      # 테이블 없으면 생성
        init_item_status()   # 상품 상태 기본 데이터 삽입


    # Blueprint 등록(오늘수정)
    from .views import (
        main_view,
        auth_view,
        product_view,
        favorite_view,
        deal_view,
        review_view,
    )

    # 메인 뷰 등록 (기본 주소 '/')
    app.register_blueprint(main_view.bp)

    # 다른 뷰들과의 충돌을 방지하기 위해 prefix를 명시적으로 붙여주는 것이 안전합니다.
    app.register_blueprint(auth_view.bp, url_prefix='/auth')
    app.register_blueprint(product_view.bp, url_prefix='/items')

    # (선택사항) 나머지 주석 처리된 것들도 나중에 쓸 때 이렇게 등록하세요.
    # app.register_blueprint(favorite_view.bp, url_prefix='/favorite')
    # app.register_blueprint(deal_view.bp, url_prefix='/deal')
    # app.register_blueprint(review_view.bp, url_prefix='/review')

    return app


