from app01 import app, db
from models import User

def init_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("数据库表已经重建")

        test_user = User(username='testuser')
        test_user.set_password('1234567')
        db.session.add(test_user)
        db.session.commit()
        print("测试用户已经创建(用户名: testuser, 密码: 1234567)")

        user = User.query.filter_by(username='testuser').first()
        if user and user.check_password('1234567'):
            print("密码验证成功")
        else:
            print("密码验证失败")
        
        return user

if __name__ == '__main__':
    init_database()
    print("数据库已经初始化完成")