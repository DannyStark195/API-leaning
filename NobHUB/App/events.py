from flask_socketio import SocketIO
from flask import request, session, current_app, flash
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room, close_room, send
from .models import User, Messages, nob_db
socketio = SocketIO()
active_users ={} 
chat_spaces = {}
@socketio.on("connect")
def handle_connect(data, auth=None):
    if current_user.is_authenticated:
        user_id = current_user.id
        username = current_user.username
        chat_space = session.get('chat_space')
        if not chat_space in chat_spaces:
            leave_room(chat_space)
            return
        join_room(chat_space)
        emit({'username': username, "message": "is online"}, to=chat_space)
        chat_spaces[chat_space]["users"]+=1
        chat_spaces[chat_space]["username"].append(username)
        print(f"{username} has joined chat space {chat_space}")

        # active_users[request.sid] ={'user_id': user_id, 'username': username}
        # chat_spaces.setdefault('global_chat', []).append(request.sid)
        #join_room('global_chat')
        
        print("User connected")
    return
@socketio.on('disconnect')
def handle_disconnect(sid=None):
    if current_user.is_authenticated:
        username= current_user.username
        chat_space = session.get('chat_space')
        leave_room(chat_space)
        if chat_space in chat_spaces:
            chat_spaces[chat_space]["users"]-=1
            chat_spaces[chat_space]["username"].remove(username)
            if chat_spaces[chat_space]["users"] <=0 :
                chat_spaces.pop(chat_space)
        send({'username': username, 'message': "is offline"}, to=chat_space)
        print(f"{username} has left chat space {chat_space}")
    # if request.sid in active_users:
    #     active_users.pop(request.sid)

@socketio.on('send-message')
def handle_send_message(data):
    if not current_user.is_authenticated:
        return
    username = current_user.username
    chat_space = session.get('chat_space')
    user_message = data['data']
    print(user_message)

    
    # contact_id = data.get('contact_id')
    # user_message = data.get('user_message')
    contact_id = session.get('contact_id')
    contact_name = session.get('contact_name')
    chat_messages = Messages(user_id=current_user.id, contact_id=contact_id, message=user_message)
    
    try:
        nob_db.session.add(chat_messages)

        nob_db.session.commit()
        chat_message = Messages.query.filter_by(user_id=current_user.id, contact_id=contact_id, message=user_message).first()
        print(chat_message.message)
        chat_message = Messages.query.filter_by(user_id=current_user.id, contact_id=contact_id, message=user_message).first()
        timestamp = chat_message.time.strftime('%Y-%m-%d %H:%M')
        message_data={
            'user_id': current_user.id,
            'username': current_user.username,
            'contact_id': contact_id,
            'message': user_message,
            'time': timestamp
            }
        emit('send-message', message_data, to=chat_space)
        
        print(f"{username}: Message: {user_message}")
        #emit('new-message', message_data, chats=)
    except Exception as e:
        nob_db.session.rollback()
        print(e)
        return 
    
    
    