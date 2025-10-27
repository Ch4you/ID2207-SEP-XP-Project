import pytest
from app import create_app
from app.db import db # 导入我们的内存数据库

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": "testing-key" # TDD时使用固定的key
    })
    
    # 在每次测试前清空内存数据库
    db['event_requests'].clear()
    db['staffing_requests'].clear()
    db['financial_requests'].clear()
    # (重置ID计数器)
    from app.models import EventPlanningRequest
    EventPlanningRequest._id_counter = 1

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()