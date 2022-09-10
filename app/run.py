from app import app, db
import views
from settings import HOST, PORT

if __name__ == '__main__':
    db.create_all(app=app)
    app.run(HOST, PORT, debug=True)
