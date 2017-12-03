import flask
from flask import Flask, render_template, request, url_for, \
	session, redirect, abort, flash
from diksha import app, db
from config import Auth
from requests_oauthlib import OAuth2Session
from flask_login import LoginManager, login_required, login_user, \
    logout_user, current_user, UserMixin
from requests.exceptions import HTTPError
from models import *

from datetime import datetime

import json

def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth

@app.route('/')
def index():
	return flask.render_template('index.html')

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('login_page.html', auth_url=auth_url)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/gCallback')
def callback():
    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        # Execution reaches here when user has
        # successfully authenticated our app.
        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            domain = email.split("@")[1]
            if domain == 'iiita.ac.in':
	            user = User.query.filter_by(email=email).first()
	            if user is None:
	                user = User()
	                user.email = email
	            user.name = user_data['name']
	            user.tokens = json.dumps(token)
	            user.avatar = user_data['picture']
	            db.session.add(user)
	            db.session.commit()
	            login_user(user)
	            return redirect(url_for('index'))
            return redirect(url_for('login'))
        return 'Could not fetch your information.'

@app.route('/booking/',methods = ['GET','POST'])
@login_required
def booking():
    print request.method

    if request.method == 'POST':
    	no_of_rooms = int(request.form['rooms'])
    	room_type = request.form['room_type']
    	room_count = Rooms.query.filter_by(availability='YES').filter_by(ac=room_type).count()
        if room_count >= no_of_rooms:
        	print "I am here"
	    	reservation=Reservation(
	    			        user_id=current_user.id,
	    			        is_cancelled=0,
	    			        check_in=request.form['arrival'],
	    			        check_out= request.form['departure']
	    			        )
    		
    		db.session.add(reservation)
    		db.session.commit()

    		arrival = datetime.strptime(request.form['arrival'], "%d %B, %Y")
    		departure = datetime.strptime(request.form['departure'], "%d %B, %Y")

    		print (departure-arrival).days
	    	booking = Booking(
	    		    name = request.form['first_name'],
	    		    reservation_id = reservation.reservation_id,
	    		    no_of_rooms = request.form['rooms'],
	    		    amount = 0
	    		    )
	    	db.session.add(booking)
	    	db.session.commit()
	    	amount = 0
        	for i in range(no_of_rooms):
	    		room=Rooms.query.filter_by(availability='YES').filter_by(ac=room_type).first()
	    		room.availability='NO'
	    		rr = RoomReservations(
	    				room_id=room.room_id,
	    				reservation_id=reservation.reservation_id
	    			)
	    		amount += room.cost_per_day * (departure-arrival).days
	    		booking.amount = amount
	    		db.session.add(rr)
	    		db.session.commit()

    		
	    	return flask.render_template('booking_success.html', 
	    		reservation_id=reservation.reservation_id,
	    		amount=amount)
        else:
	    	return flask.render_template('booking_failure.html')

	    	print Rooms.query.filter_by(availability='YES').count()
	        print request.form


    return flask.render_template('booking.html')



@app.route('/cancellation/',methods = ['GET','POST'])
@login_required
def cancellation():

	if request.method == 'POST':
		print request.form['invoice_id']
		cancellation=Cancellation(
		    	invoice_id=request.form['invoice_id']
		    	)
		db.session.add(cancellation)
		booking=Booking.query.filter_by(invoice_id=request.form['invoice_id']).first()
		reservation=Reservation.query.filter_by(reservation_id=booking.reservation_id).first()
		reservation.is_cancelled=1
		rr = RoomReservations.query.filter_by(reservation_id=reservation.reservation_id).all()
		for room in rr:

			room=Rooms.query.filter_by(room_id=room.room_id).first()
			room.availability='YES'
			db.session.commit()
        flash("Reservation has been cancelled successfully", "success")

	return flask.render_template('cancellation.html')

@app.route('/reservation/',methods = ['GET','POST'])
@login_required
def reservation():
    if request.method == 'GET':

        reservations=Reservation.query.filter_by(user_id=current_user.id).all()
        data=[]
        for reservation in reservations:
            booking=Booking.query.filter_by(reservation_id=reservation.reservation_id).first()
            rooms = RoomReservations.query.filter_by(reservation_id=reservation.reservation_id).all()
            dict_={
                "reservation":reservation,
                "booking":booking,
                "rooms": rooms
            }
            data.append(dict_)

        print reservations
    return flask.render_template('reservation.html',data=data)

@app.route('/admin/reservations/',methods = ['GET'])
@login_required
def admin_reservation():

    if current_user.email != 'iit2014035@iiita.ac.in':
	    abort(404)
    if request.method == 'GET':
        reservations=Reservation.query.all()
        data=[]
        for reservation in reservations:
            booking=Booking.query.filter_by(reservation_id=reservation.reservation_id).first()
            rooms = RoomReservations.query.filter_by(reservation_id=reservation.reservation_id).all()
            dict_={
                "reservation":reservation,
                "booking":booking,
                "rooms": rooms
            }
            data.append(dict_)
    return flask.render_template('reservation.html',data=data, is_admin=1)

@app.route('/admin/rooms/',methods = ['GET', 'POST'])
@login_required
def admin_room():

    if current_user.email != 'iit2014035@iiita.ac.in':
	    abort(404)
    if request.method == 'POST':
    	room = Rooms(
    			availability="YES",
    			hostel_number=int(request.form['hostel']),
    			ac=request.form['room_type'],
    			cost_per_day=int(request.form['cost'])
    		)
    	db.session.add(room)
    	db.session.commit()

    	flash("New Room added", "success")
    return flask.render_template('room.html')
