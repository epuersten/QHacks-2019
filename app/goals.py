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


@app.route('/goals')
@login_required
def goals():
    return render_template('goals.html', async_mode=None)

