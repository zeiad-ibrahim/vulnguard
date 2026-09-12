import sqlite3
import os
# Import bcrypt for password hashing
import bcrypt

databasepath = os.path.join(os.path.dirname(__file__), "users.db")

class database:
    # Initialize the Database class with the database path
    def __init__(self, databasepath):
        self.databasepath = databasepath # Store the database path
        self.conn = sqlite3.connect(self.databasepath) # Connect to the database
        self.cursor = self.conn.cursor() # Create a cursor for database operations

    # Method to create and initialize the users table
    def create(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT UNIQUE NOT NULL, 
                hashed_pass TEXT NOT NULL
            )
        """) # Create the users table with both password and hashed_pass columns
        self.conn.commit() # Commit the changes to the database
        self.conn.close() # Close the database connection
        print("Database 'users.db' initialized with 'users' table.") # Print confirmation message to allow me know everything is working fine

    
    def vulcreate(self):#  method to create the vulnerability database
        vuln_database_path = os.path.join(os.path.dirname(self.databasepath), "vulnerability.db") # this is the path for vulnerability.db in the same directory as users.db
        conn = sqlite3.connect(vuln_database_path)
        cursor = conn.cursor()

        # Create the vulnerabilities table with the following coloumns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                port INTEGER PRIMARY KEY,
                service TEXT,
                vulnerabilities TEXT,
                recommendations TEXT
            )
        ''')

        # Format is (port, service, vulnerabilities, recommendations)
        vulnerability_data = [
            (21, "ftp", "Anonymous FTP login allowed, Potential brute force attack risk", 
             "Disable anonymous FTP, Use strong passwords and enforce rate limiting"),
            (22, "ssh", "Weak SSH key algorithms (e.g., SHA-1), Potential brute force attack risk", 
             "Use modern key algorithms (e.g., Ed25519), Enable two-factor authentication, Use SSH keys instead of passwords"),
            (23, "telnet", "Unencrypted communication, High risk of credential sniffing", 
             "Use encrypted protocols (e.g., SSH instead of Telnet), Enable HTTPS"),
            (25, "smtp", "Potential brute force attack risk, Unencrypted communication", 
             "Use encrypted protocols (e.g., SMTPS), Enable two-factor authentication"),
            (53, "domain", "DNS cache poisoning, Zone transfer attacks", 
             "Restrict zone transfers, Use DNSSEC"),
            (80, "http", "Weak SSL/TLS configurations, Outdated cipher suites", 
             "Use modern TLS versions (e.g., TLS 1.3), Disable weak ciphers"),
            (111, "rpcbind", "Potential RPC-based attacks, Known vulnerabilities in older versions", 
             "Restrict RPC access, Keep software updated"),
            (139, "netbios-ssn", "Susceptible to SMBv1 exploits, Potential ransomware attack vector", 
             "Disable SMBv1, Use SMBv3 with encryption"),
            (445, "microsoft-ds", "Susceptible to SMBv1 exploits, Potential ransomware attack vector", 
             "Disable SMBv1, Use SMBv3 with encryption"),
            (512, "exec", "Unencrypted communication, High risk of credential sniffing", 
             "Use encrypted alternatives, Restrict access via firewall"),
            (513, "login", "Unencrypted communication, High risk of credential sniffing", 
             "Use encrypted alternatives, Restrict access via firewall"),
            (514, "shell", "Unencrypted communication, High risk of credential sniffing", 
             "Use encrypted alternatives, Restrict access via firewall"),
            (1099, "rmiregistry", "Known vulnerabilities in older versions, RMI deserialization attacks", 
             "Keep software updated, Restrict access via firewall"),
            (1524, "ingreslock", "Known vulnerabilities in older versions, Backdoor access", 
             "Keep software updated, Restrict access via firewall"),
            (2049, "nfs", "Weak NFS permissions, File access vulnerabilities", 
             "Restrict NFS access, Use strong permissions"),
            (2121, "ccproxy-ftp", "Potential brute force attack risk, Unencrypted communication", 
             "Use encrypted protocols, Enable two-factor authentication"),
            (3306, "mysql", "Potential SQL injection, Weak authentication methods", 
             "Use strong passwords, Enable SSL for MySQL connections"),
            (5432, "postgresql", "Potential SQL injection, Weak authentication methods", 
             "Use strong passwords, Enable SSL for PostgreSQL connections"),
            (5900, "vnc", "Known vulnerabilities in older VNC versions, Weak encryption", 
             "Use strong passwords, Enable strong encryption"),
            (6000, "X11", "Unencrypted communication, Unauthorized access", 
             "Use SSH tunneling for X11, Restrict access via firewall"),
            (6667, "irc", "Unencrypted communication, Potential DoS attacks", 
             "Use encrypted protocols, Restrict access via firewall"),
            (8180, "ajp13", "AJP protocol vulnerabilities, Information disclosure", 
             "Disable AJP if not needed, Restrict access via firewall"),
            (0, "unknown", "Unknown service/port", 
             "Investigate and close if not needed, Restrict access via firewall")
        ]

        # to add the vulnerability data into the table
        cursor.executemany('''
            INSERT OR REPLACE INTO vulnerabilities (port, service, vulnerabilities, recommendations)
            VALUES (?, ?, ?, ?)
        ''', vulnerability_data)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

# define a user class whichc will be responsible to carry out user operations on the database
class User_op:
    def __init__(self, databasepath): # Initialize the User class with the database path
        self.databasepath = databasepath # Store the database path in a variable
        self.conn = sqlite3.connect(self.databasepath) # Connect to the database
        self.cursor = self.conn.cursor() # Create a cursor to be able to carry out database operations whihc i will use later

    # Method to hash the password using bcrypt
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) # encrpyt the password

    # Method to verify the password against the stored hash
    def verify_password(self, password, hashed_pass): # verify the password against the stored hash
        return bcrypt.checkpw(password.encode('utf-8'), hashed_pass) # hashes the password and compares it to the stored hash password

    # Method to sign up a user with both plain and hashed password
    def signup(self, email, password):
        try:
            # Check if this email is already used
            self.cursor.execute("SELECT email FROM users WHERE email = ?", (email,)) # searchs through the database for the email
            if self.cursor.fetchone() == (email,): # if the email is already in the database
                return False, "That email is already taken, please use a different one" # return this error message

            hashed_pass = self.hash_password(password) # hash the password
            self.cursor.execute("INSERT INTO users (email, hashed_pass) VALUES (?, ?)", (email, hashed_pass)) # insert the email, password, and hashed password  into the database
            self.conn.commit() #save the changes to the database
            print("User", email, "saved in database") # print this message
            return True, None 

        except sqlite3.OperationalError as e: # if there is an operational error
            print("Database problem") # print this message
            return False, "Database error occurred, please try again" # return this error message
        except sqlite3.IntegrityError as e: # if there is an integrity error
            print("Database problem with data") # print this message
            return False, "Database integrity issue, please try again" # return this error message
        except Exception as e: # if there is any other error
            print("Unexpected error") # print this message
            return False, "Something unexpected happened, please try again" # return this error message

    # method to check if the email is already in the database with the correct password
    def login(self, email, password):
        self.cursor.execute("SELECT hashed_pass FROM users WHERE email = ?", (email,)) # searchs through the database for the email
        result = self.cursor.fetchone() # fetches the result of the query
        if result:
            hashed_pass = result[0] # get the stored hashed password 
            if self.verify_password(password, hashed_pass): # verify the provided password against the hashed password
                return True # if the password matches, return True
            else:
                return False # if the password doesn't match, return False
        return False # if the user is not found, return False

    # Method to close the database connection
    def close(self):
        self.conn.close()