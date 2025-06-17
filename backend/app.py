from flask import Flask
from config import Config
from models import db
from flask_migrate import Migrate


# Initialize Flask app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return 'Hello Everyone'

if __name__ == '__main__':
    app.run(debug=True)
