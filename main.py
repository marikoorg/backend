from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configure the database connection using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Message model
class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def is_alive():
    return jsonify('live')


@app.route('/api/msg/<string:msg>', methods=['POST'])
def msg_post_api(msg):
    print(f"msg_post_api with message: {msg}")

    # A message instance
    new_message = Message(message=msg)
    db.session.add(new_message)
    db.session.commit()

    msg_id = new_message.id
    
    return jsonify({'msg_id': msg_id})


@app.route('/api/msg/<int:msg_id>', methods=['GET'])
def msg_get_api(msg_id):
    print(f"msg_get_api > msg_id = {msg_id}")

    msg = Message.query.get(msg_id)
    
    # Check if message is not found
    if not msg:
        return jsonify({'error': 'Message not found'}), 404
        
    return jsonify({'msg': msg})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
