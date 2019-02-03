#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import NetUser


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
socketio.run(app)


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1


# Chat Features
#--------------------------------------------------------------------------
@app.route('/chat')
@login_required
def chat():
    user_id = current_user.user_id
    user = NetUser.query.filter_by(user_id=user_id).first_or_404()
    return render_template('chat.html', async_mode=socketio.async_mode, user=user)


@socketio.on('join', namespace='/test')
def join(message):
   join_room(message['room'])
   session['receive_count'] = session.get('receive_count', 0) + 1
   emit('my_response',
        {'data': 'joined room: ' + message['room'],
         'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
   leave_room(message['room'])
   session['receive_count'] = session.get('receive_count', 0) + 1
   emit('my_response',
        {'data': 'left room: ' + message['room'],
         'count': session['receive_count']})


@socketio.on('close_room', namespace='/test')
def close(message):
   session['receive_count'] = session.get('receive_count', 0) + 1
   emit('my_response', {'data': 'closed room: ' + message['room'],
                        'count': session['receive_count']},
        room=message['room'])
   close_room(message['room'])


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
   session['receive_count'] = session.get('receive_count', 0) + 1
   emit('my_response',
        {'data': 'posted in ' + message['room'] + ': ' + message['data'], 'count': session['receive_count']},
        room=message['room'])


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


#Connect Features
#--------------------------------------------------------------------------
@app.route('/connect')
@login_required
def connect():
    return render_template('connect.html', async_mode=socketio.async_mode)

@socketio.on('search', namespace='/test2')
def search(message):
    if (message['first_name_bool']):
        if (message['last_name_bool']):
            if (message['school_bool']):
                if (message['program_bool']):
                    users = NetUser.query.filter_by(first_name=message['first_name_search']).filter_by(last_name=message['last_name_search']).filter_by(school_name=message['school_search']).filter_by(program_name=message['program_search']).all()
                    print("searched by first name, last name, school, and program")
                else:
                    users = NetUser.query.filter_by(first_name=message['first_name_search']).filter_by(last_name=message['last_name_search']).filter_by(school_name=message['school_search']).all()
                    print("searched by first name, last name, and school")
            else:
                if (message['program_bool']):
                    users = NetUser.query.filter_by(first_name=message['first_name_search']).filter_by(last_name=message['last_name_search']).filter_by(program_name=message['program_search']).all()
                    print("searched by first name, last name, and program")
                else:
                    users = NetUser.query.filter_by(first_name=message['first_name_search']).filter_by(last_name=message['last_name_search']).all()
                    print("searched by first name and last name")
        else:
            if (message['school_bool']):
                if (message['program_bool']):
                    users = NetUser.query.filter_by(first_name=message['first_name_search']).filter_by(school_name=message['school_search']).filter_by(program_name=message['program_search']).all()
                    print("searched by first name, school, and program")
                else:
                    users = NetUser.query.filter_by(first_name=message['first_name_search']).filter_by(school_name=message['school_search']).all()
                    print("searched by first name and school")
            else:
                if (message['program_bool']):
                    users = NetUser.query.filter_by(first_name=message['first_name_search']).filter_by(program_name=message['program_search']).all()
                    print("searched by first name and program")
                else:
                    users = NetUser.query.filter_by(first_name=message['first_name_search']).all()
                    print("searched by first name")
    else:
        if (message['last_name_bool']):
            if (message['school_bool']):
                if (message['program_bool']):
                    users = NetUser.query.filter_by(last_name=message['last_name_search']).filter_by(school_name=message['school_search']).filter_by(program_name=message['program_search']).all()
                    print("searched by last name, school, and program")
                else:
                    users = NetUser.query.filter_by(last_name=message['last_name_search']).filter_by(school_name=message['school_search']).all()
                    print("searched by last name, and school")
            else:
                if (message['program_bool']):
                    users = NetUser.query.filter_by(last_name=message['last_name_search']).filter_by(program_name=message['program_search']).all()
                    print("searched by last name, and program")
                else:
                    users = NetUser.query.filter_by(last_name=message['last_name_search']).all()
                    print("searched by last name")
        else:
            if (message['school_bool']):
                if (message['program_bool']):
                    users = NetUser.query.filter_by(school_name=message['school_search']).filter_by(program_name=message['program_search']).all()
                    print("searched by school and program")
                else:
                    users = NetUser.query.filter_by(school_name=message['school_search']).all()
                    print("searched by school")
            else:
                if (message['program_bool']):
                    users = NetUser.query.filter_by(program_name=message['program_search']).all()
                    print("searched by program")
                else:
                    users = NetUser.query.all()
                    print("not searched")

    for i in range(len(users)):
        emit('my_response',{'first_name': users[i].first_name,'last_name':users[i].last_name, 'school':users[i].school_name ,'program':users[i].program_name, 'courses':message['course_search']})
