import mysql.connector as mysql


class UserDB:
    user = "root"
    password = "password"
    host = "db"

    def __enter__(self):
        self.con = mysql.connect(
            user=self.user, password=self.password, host=self.host, database="users"
        )
        self.cur = self.con.cursor()
        return self


    def __exit__(self, *args):
        self.cur.close()
        self.con.commit()
        self.con.close()

    def setup(self):
        con = mysql.connect(user="root", password="password", host="db")
        cur = con.cursor()

        cur.execute("CREATE DATABASE IF NOT EXISTS users")
        cur.execute("USE users")

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL,
        hashpass TEXT NOT NULL,
        id INT NOT NULL AUTO_INCREMENT UNIQUE,
        PRIMARY KEY (id)
        )
        """
        )

        cur.close()
        con.close()

    def get_user_info(self, username: str):
        """
        gets the user info from the username in the database

        args:
            username:
                type: String
                represents the username to be found inside the database

        returns:
            (username, hashpass)
        """
        self.cur.execute("SELECT * FROM users WHERE username = %s", (username,))

        data = self.cur.fetchone()

        if data:
            return str(data[0]), str(data[1]), str(data[2])
        return None

    def get_user_id(self, id: str):
        int_id = int(id)

        self.cur.execute("SELECT * FROM users WHERE id=%s", (int_id,))

        user = self.cur.fetchone()

        if user:
            return str(user[0]), str(user[1]), str(user[2])
        return None

    def add_user(self, username: str, password: str):
        self.cur.execute("SELECT * FROM users WHERE username = %s", (username,))

        data = self.cur.fetchone()
        if data is None:
            self.cur.execute("INSERT INTO users (username, hashpass) VALUES (%s, %s)", (username, password))
            return True
        else:
            return False

    def add_win(self, userid, won):
        pass

    def add_auc(self, userid, auc_name, price):
        pass
