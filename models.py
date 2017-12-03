from diksha import db
import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

class Guest(db.Model):
    __tablename__ = "guest"
    guest_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    relation = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone_num = db.Column(db.Integer)
    age = db.Column(db.Integer)

    def __init__(self, name, address, relation, phone_num, age):
        self.name = name
        self.address = address
        self.relation = relation
        self.phone_num=phone_num
        self.age=age

    def __repr__(self):
        return '<Name %r>' % self.name

class Booking(db.Model):
    __tablename__ = "booking"
    reservation_id = db.Column(db.Integer)
    invoice_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    no_of_rooms = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    def __init__(self, reservation_id, name, no_of_rooms, amount):
        self.reservation_id = reservation_id
        self.name=name
        self.no_of_rooms=no_of_rooms
        self.amount=amount

    def __repr__(self):
        return '<name %r>' % self.name


class Reservation(db.Model):
    __tablename__ = "reservation"
    reservation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    is_cancelled = db.Column(db.Integer)
    check_in = db.Column(db.String(120))
    check_out = db.Column(db.String(120))

    def __init__(self, check_in, check_out, user_id, is_cancelled):
        self.check_in = check_in
        self.check_out = check_out
        self.user_id = user_id
        self.is_cancelled = is_cancelled


    def __repr__(self):
        return '<reservation_id %r>' % self.reservation_id

class RoomReservations(db.Model):
    __tablename__ = "room_reservation_map"
    rr_id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer)
    room_id = db.Column(db.Integer)


class Cancellation(db.Model):
    __tablename__ = "cancellation"
    cancellation_id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer)

    def __init__(self,invoice_id):
        self.invoice_id = invoice_id

    def __repr__(self):
        return '<invoice_id %r>' % self.invoice_id


class Rooms(db.Model):
    __tablename__ = "rooms"
    room_id = db.Column(db.Integer, primary_key=True)
    availability = db.Column(db.String(120))
    cost_per_day = db.Column(db.Integer)
    ac=db.Column(db.String(120))
    hostel_number = db.Column(db.Integer)

    def __init__(self, availability, cost_per_day, ac, hostel_number):
        self.availability = availability
        self.cost_per_day = cost_per_day
        self.ac = ac
        self.hostel_number = hostel_number

    def __repr__(self):
        return '<availability %r>' % self.availability