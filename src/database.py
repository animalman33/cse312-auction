import mysql.connector as mysql


class Database:
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
            userID INT NOT NULL AUTO_INCREMENT UNIQUE,
            PRIMARY KEY (userID)
        )
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS auctions (
            name TEXT NOT NULL,
            cost INT NOT NULL,
            startcost INT NOT NULL,
            completed BOOLEAN,
            userID INT,
            aucID INT NOT NULL AUTO_INCREMENT UNIQUE,
            PRIMARY KEY (aucID),
            FOREIGN KEY (userID) REFERENCES users(userID)
        )
        """
        )
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS bids (
            amount INT NOT NULL,
            bidID INT NOT NULL AUTO_INCREMENT UNIQUE,
            aucID INT,
            userID INT,
            PRIMARY KEY (bidID),
            FOREIGN KEY (userID) REFERENCES users(userID),
            FOREIGN KEY (aucID) REFERENCES auctions(aucID)
        )
        """
        )
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS wins (
            amount INT NOT NULL,
            aucID INT,
            userID INT,
            FOREIGN KEY (userID) REFERENCES users(userID),
            FOREIGN KEY (aucID) REFERENCES auctions(aucID)
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

        self.cur.execute("SELECT * FROM users WHERE userID=%s", (int_id,))

        user = self.cur.fetchone()

        if user:
            return str(user[0]), str(user[1]), str(user[2])
        return None

    def add_user(self, username: str, password: str):
        self.cur.execute("SELECT * FROM users WHERE username = %s", (username,))

        data = self.cur.fetchone()
        if data is None:
            self.cur.execute(
                "INSERT INTO users (username, hashpass) VALUES (%s, %s)",
                (username, password),
            )
            return True
        else:
            return False

    def add_win(self, userid, aucid, amount):
        self.cur.execute(
            "INSERT INTO wins (amount, aucID, userID) VALUES (%s, %s, %s)",
            (amount, aucid, userid),
        )

    def add_auc(self, userid, auc_name, start_price) -> bool:
        """
        adds an auction to the database
        if the auctions already exists false is returned
        otherwise true is returned
        """
        self.cur.execute("SELECT * FROM auctions WHERE name = %s", (auc_name,))
        item = self.cur.fetchone()
        if item:
            return False
        self.cur.execute(
            "INSERT INTO auctions (name, cost, startcost, completed, userid) VALUES (%s, %s, %s, %s, %s)",
            (auc_name, start_price, start_price, False, userid),
        )
        return True

    def add_bid(self, bid_amount: int, auc_id: int, userid: int) -> bool:
        """
        attempts to add a bid to the database
        returns false if auction does not exist or is completed or bid is to low
        returns true if bid was succesful

        """

        self.cur.execute("SELECT * FROM auctions WHERE aucID=%s", (auc_id,))

        auction = self.cur.fetchone()
        """        CREATE TABLE IF NOT EXISTS bids (
            amount INT NOT NULL,
            bidID INT NOT NULL AUTO_INCREMENT UNIQUE,
            aucID INT,
            userID INT,
            PRIMARY KEY (bidID),
            FOREIGN KEY (userID) REFERENCES users(userID),
            FOREIGN KEY (aucID) REFERENCES auctions(aucID)
        )"""
        if auction is None:
            return False
        elif int(auction[1]) > bid_amount:
            return False
        else:
            self.cur.execute("INSERT INTO bids (amount, aucID, userID) VALUES (%s, %s, %s)", (bid_amount, auc_id, userid))
            self.cur.execute("UPDATE auctions SET cost=%s WHERE aucID=%s", (bid_amount, auc_id))
            return True

    def get_user_bids(self, userid: int):

        self.cur.execute("SELECT * FROM bids WHERE userID=%s ORDER BY bidID DESC LIMIT 50", (userid,))
        bids = self.cur.fetchall()
        retVal = []

        if bids:
            for x in bids:
                retVal.append({"bidID": x[0], "aucID": x[1]})
        return retVal

    def get_user_wins(self, userid: int):

        self.cur.execute("SELECT * FROM ")
