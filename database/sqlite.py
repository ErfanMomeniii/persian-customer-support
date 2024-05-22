import sqlite3
from crawl.models.flight import flight
from crawl.models.hotel import hotel


class sqllite:
    def __init__(self):
        self.cursor = None
        self.conn = None
        self.connect()
        self.flight_table()
        self.hotel_table()

    def connect(self):
        self.conn = sqlite3.connect('travel.db')
        self.cursor = self.conn.cursor()

        return

    def flight_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                leave_time DATE NOT NULL,
                airline_name TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        ''')

        return

    def hotel_table(self):
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS hotels (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        `name` TEXT NOT NULL,
                        country_name TEXT NOT NULL,
                        city_name TEXT NOT NULL,
                        price_per_night INTEGER NOT NULL,
                        adult_count INTEGER NOT NULL,
                        child_count INTEGER NOT NULL
                    )
                ''')

        return

    def create_flight(self, f: flight):
        self.cursor.execute('''
            INSERT INTO flights (origin, destination,leave_time,airline_name,price) VALUES (?,?,?,?,?)
        ''', (f.origin, f.destination, f.leave_time, f.airline_name, f.price))
        self.conn.commit()

        return

    def create_hotel(self, h: hotel):
        self.cursor.execute('''
                    INSERT INTO hotels (`name`, country_name,city_name,price_per_night,adult_count,child_count) VALUES (?,?,?,?,?,?)
                ''', (h.name, h.country_name, h.city_name, h.price_per_night, h.adult_count, h.child_count))
        self.conn.commit()

        return

    def update_flight(self, f_id: int, f: flight):
        self.cursor.execute('''
            UPDATE flights SET origin = ?,destination=?,leave_time=?,airline_name=?,price=? WHERE id = ?
        ''', (f.origin, f.destination, f.leave_time, f.airline_name, f.price, f_id))
        self.conn.commit()

        return

    def update_hotel(self, h_id: int, h: hotel):
        self.cursor.execute('''
                    UPDATE hotels SET `name` = ?,country_name=?,city_name=?,price_per_night=?,adult_count=?0,child_count=? WHERE id = ?
                ''', (h.name, h.country_name, h.city_name, h.price_per_night, h.adult_count, h.child_count, h_id))
        self.conn.commit()

        return

    def read_flights(self):
        self.cursor.execute('SELECT * FROM flights')
        flights = self.cursor.fetchall()

        return flights

    def read_hotel(self):
        self.cursor.execute('SELECT * FROM hotels')
        hotels = self.cursor.fetchall()

        return hotels

    def delete_flight(self, f_id: int):
        self.cursor.execute('''
            DELETE FROM flights WHERE id = ?
        ''', f_id)
        self.conn.commit()

        return

    def delete_hotel(self, h_id: int):
        self.cursor.execute('''
            DELETE FROM hotels WHERE id = ?
        ''', h_id)
        self.conn.commit()

        return
