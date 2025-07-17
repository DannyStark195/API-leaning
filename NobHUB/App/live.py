from flask import Flask, session, render_template, redirect, request, url_for
from flask_socketio import join_room, leave_room, SocketIO, send
import random
from string import ascii_uppercase

app = Flask(__name__)

app.config['SECRET_KEY'] = 'eweheow92ep'
blah = []
socketio = SocketIO(app)
rooms ={}
def generate_unique_code(num):
    while True:
        code =""
        for _ in range(num):
            code+= random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code
@app.route('/', methods=['POST', 'GET'])
def home():
    session.clear()
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        join = request.form.get('join', False)
        create = request.form.get('create', False)

        if not name:
            return render_template('live_home.html', error='Please enter a name', code=code, name=name)
        
        if join != False and not code:
            return render_template('live_home.html', error='Please enter a code',  code=code, name=name)
        room = code
        #room = contact.usename+current_user.username
        # rooms[room] = {'users': 0, 'messages':[]}
        #if contact.username+current_user.username not in rooms
        if create!= False:
        
            room = generate_unique_code(4)
            rooms[room] = {'users': 0, 'messages':[]}
        elif code not in rooms:
            return render_template('live_home.html', error='Room does not exist',  code=code, name=name)
      
        session['name'] = name
        session['room'] = room
        return redirect(url_for('room'))

    return render_template('live_home.html')
@app.route('/room')
def room():
    
    name = session.get('name')
    room = session.get('room')
    if not name or room not in rooms:
        return redirect(url_for('home'))
    
    blah.append('blah')

    return render_template("room.html", room=room, blah=blah)
@socketio.on('message')
def message(data):
    room = session.get('room')
    if room not in rooms:
        return
    content = {
        "name": session.get('name'),
        "message": data['data']
    }
    blah.append(data['data'])
    print(data['data'])
    send(content, to=room)
    rooms[room]['messages'].append(content)    
    print(f"{session.get('name')} said {data['data']}")
@socketio.on("connect")
def connect(auth):
    name = session.get('name')
    room = session.get('room')
    if not name or room not in rooms:
        return 
    
    if room not in rooms:
        leave_room(room)
        return
    join_room(room)
    send({'name': name, "message": 'has entered room'}, to=room) #we could flash messages flash('username is online')
    rooms[room]["users"] +=1
    print(f"{name} has joined room {room}")
@socketio.on("disconnect")
def disconnect():
    name = session.get('name')
    room = session.get('room')
    leave_room(room)

    if room in rooms:
        rooms[room]['users']-=1
        if rooms[room]['users'] <=0:
            del rooms[room]
    send({"name":name, "message": "has left room"})
    print(f"{name} has left room {room}")

if __name__ == "__main__":
    socketio.run(app, debug=True)