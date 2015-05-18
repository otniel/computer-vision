import sqlite3 as lite


class SolidAttendanceDao:
    def __init__(self):
        pass

    def insert_new_user(self, name, charge):
        conn = lite.connect('solid_attendance.db')
        sql = "INSERT INTO users(name, charge) VALUES (?, ?)"
        with self.conn:
            cur = conn.cursor()
            cur.execute(sql, (name, charge))
            conn.commit()

    def get_users(self):
        sql = "SELECT * FROM users"
        conn = lite.connect('solid_attendance.db')
        with conn:
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def get_last_user_id(self):
        users = self.get_users()
        if users:
            return users[-1][0]
        return 0

    def get_user_by_id(self, id_user):
        conn = lite.connect('solid_attendance.db')
        sql = "SELECT * FROM users WHERE id=" + str(id_user)
        with conn:
            cur = conn.cursor()
            cur.execute(sql)
            user = cur.fetchall()
            name, charge = user[0][1], user[0][2]
            return name, charge