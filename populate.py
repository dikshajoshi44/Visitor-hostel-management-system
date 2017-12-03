from diksha import db
from models import Rooms

# hostel 1: 20 Non AC, 10 AC
for i in range(25):
	rooms = Rooms(
			availability="YES",
			cost_per_day=300,
			ac="NONAC",
			hostel_number=1
		)

	db.session.add(rooms)
	db.session.commit()
for i in range(10):
	rooms = Rooms(
			availability="YES",
			cost_per_day=500,
			ac="AC",
			hostel_number=1
		)

	db.session.add(rooms)
	db.session.commit()

# hostel 2: 5 Non AC, 3 AC
for i in range(5):
	rooms = Rooms(
			availability="YES",
			cost_per_day=300,
			ac="NONAC",
			hostel_number=2
		)
	db.session.add(rooms)
	db.session.commit()
for i in range(3):
	rooms = Rooms(
			availability="YES",
			cost_per_day=500,
			ac="AC",
			hostel_number=2
		)
	db.session.add(rooms)
	db.session.commit()

# hostel 3: 10 AC
for i in range(10):
	rooms = Rooms(
			availability="YES",
			cost_per_day=500,
			ac="AC",
			hostel_number=3
		)
	db.session.add(rooms)
	db.session.commit()
