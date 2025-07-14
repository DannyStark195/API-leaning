from flask_socketio import SocketIO
from flask import request, session, current_app, flash
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room, close_room
from .models import User, Messages, nob_db
socketio = SocketIO()
active_users ={} 
chats = {}
@socketio.on("connect")
def handle_connect():
    if current_user.is_authenticated():
        user_id = current_user.id
        username = current_user.username
        active_users[request.sid] ={'user_id': user_id, 'username': username}
        chats.setdefault('global_chat', []).append(request.sid)
        join_room('global_chat')
    print("User connected")
@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in active_users:
        active_users.pop(request.sid)

@socketio.on('send-message')
def handle_send_message(data):
    if not current_user.is_authenticated:
        return

    
    contact_id = data.get('contact_id')
    user_message = data.get('user_message')

    chat_messages = Messages(user_id=current_user.id, contact_id=contact_id, message=user_message)
    
    try:
        nob_db.session.add(chat_messages)
        nob_db.commit()
        message_data={
            'user_id': current_user.id,
            'username': current_user.username,
            'contact_id': contact_id,
            'message': user_message,

        }

        emit('new-message', username=current_user.username, contact_id=contact_id, message=chat_messages)
    except:
        nob_db.session.rollback
    