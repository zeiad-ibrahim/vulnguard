from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from users import database  # Import the database initialization function from users.py
from users import User_op  # Import the user class from user.py
# Import python-nmap for real network scanning
import nmap

website = Flask(__name__)

# stores the database path which will be used for storing user data
databasepath = os.path.join(os.path.dirname(__file__), "users.db")

# Call the functon that creates and initialises the databasefrom users.py 
db = database(databasepath)
db.create() # This ensures users.db is created by users.py (this is where the database is created)

@website.route('/signup', methods=['POST'])
def signup():
    input_data = request.get_json() # gets data from the javascript of the form in the signup.html file
    email = input_data.get('email', '').strip()  # gets the inputted email and removes any extra spaces
    password = input_data.get('password', '').strip() # gets the inputted password and removes any extra spaces
    confirm_password = input_data.get('confirm_password', '').strip() # gets the inputted confirm password and removes any extra spaces
    
    if email == "": # Check if email field is left empty
        return jsonify({"success": False, "error": "Please make sure the email field isn't left empty"}), 400 #if it is empty, return an error message
    
    if password == "": # check if password field is left empty
        return jsonify({"success": False, "error": "Please make sure the password field isn't left empty"}), 400 # if it is empty, return an error message

    if confirm_password == "": # check if confirm password field is left empty
        return jsonify({"success": False, "error": "Please make sure the confirm password field isn't left empty"}), 400 # if it is empty, return an error message

    if len(password) < 8: # checks if password length is less than 8 characters
        return jsonify({"success": False, "error": "Password needs to be at least 8 characters long"}), 400 # if it is less than 8 characters, return an error message

    # the next few lones of code is to check if password has one uppercase letter, one lowercase letter, and one number
    uppercase = False # will be used to check uppercase letters
    lowercase = False # will be used to check lowercase letters
    number = False # will be used to check numbers
    for char in password: # runs the for loop unction for every character in the password
        if char >= 'A' and char <= 'Z': # checks if the character is an uppercase letter
            uppercase = True # if it is, set uppercase variable to True
        elif char >= 'a' and char <= 'z': # checks if the character is a lowercase letter
            lowercase = True # if it is, set lowercase variable to True
        elif char >= '0' and char <= '9': # checks if the character is a number
            number = True # if it is, set number variable to True
    if uppercase == False or lowercase == False or number == False: # checks if any of the uppercase, lowercase, or number variables are False
        return jsonify({"success": False, "error": "Password needs at least one uppercase letter, one lowercase letter, and one number"}), 400 # if any of the variables are False, return an error message

    if password != confirm_password: # checks if the password and confirm password fields are the same
        return jsonify({"success": False, "error": "The passwords don't match, please check and try again"}), 400 # if they are not the same, return an error message

    user = User_op(databasepath) # stores the user class in a variable and makes it point to the database  so that operations can be carried out on the database
    success, error_message = user.signup(email, password) # Attempt to sign up the user using the User_op class
    user.close() # closes the database
    
    if success:
        return jsonify({"success": True}), 200 # Return success message
    else:
        return jsonify({"success": False, "error": error_message}), 400 # Return error message

# Define a route for handling login requests
@website.route('/login', methods=['GET', 'POST'])
# Define the login function
def login():
    if request.method == 'POST': # Check if the request is a POST request
        input_data = request.get_json() # requests the data from the form in the login.html file
        email = input_data.get('email', '').strip() # gets the inputted email and removes any extra spaces
        password = input_data.get('password', '').strip() # gets the inputted password and removes any extra spaces
        user = User_op(databasepath) # stores the user class in a variable and makes it point to the database  so that operations can be carried out on the database

        if email == "": # Check if email field is left empty for exception handling
            return jsonify({"success": False, "error": "Please make sure the email field isn't left empty"}), 400 #if it is empty, return an error message
    
        elif password == "": # check if password field is left empty for exception handing
            return jsonify({"success": False, "error": "Please make sure the password field isn't left empty"}), 400 # if it is empty, return an error message

        elif user.login(email, password): # checks if the email and password are in the database
            user.close() # closes the database
            return jsonify({"success": True}), 200 # if the email and password are in the database return a success message
        else:
            user.close() # closes the database
            return jsonify({"success": False, "error": "Invalid email or password"}), 401 # if the email and password are not in the database return an error message

    return render_template('login.html') # if the request is not a POST request, render the login.html template

@website.route('/mainpage')
# Define the mainpage function to handle homepage requests
def mainpage():
    return render_template('mainpage.html')  # Render the mainpage.html template

# Define a route for the login page
@website.route('/logout')
# Define the login function to handle login page requests
def logout():
    return render_template('login.html')  # Render the login.html template

@website.route('/')
def dashboard():
    # Show the signup page when someone visits the site
    return render_template('signup.html')

# Define a route for the full system scan page
@website.route('/fullscan')
def fullscan():
    return render_template('fullscan.html')

# Define a route for the targeted system scan page
@website.route('/targetedscan')
def targetedscan():
    return render_template('targeted.html')

# Define a route for the scan history page
@website.route('/history')
def history():
    return render_template('history.html')

# Define a route for the settings page
@website.route('/settings')
def settings():
    return render_template('settings.html')




def dbvulnerability(port):  # Function to search the database for identified vulnerabilities
    conn = sqlite3.connect('vulnerabilities.db')# Connect to the SQLite database
    cursor = conn.cursor()

    cursor.execute('SELECT vulnerabilities, recommendations FROM vulnerabilities WHERE port = ?', (port,))# search vulnerabilities for the specific port that was found open
    result = cursor.fetchone()

    # If no specific vulnerabilities are found for the port, use the default (port 0) which contains general recommendations
    if not result:
        cursor.execute('SELECT vulnerabilities, recommendations FROM vulnerabilities WHERE port = 0')
        result = cursor.fetchone()
    conn.close()

    if result:
        if result[0]: # checks if there are any vulnerabilities found
            vulnerabilities = result[0].split(', ')  
        else:
            vulnerabilities = ["No specific vulnerabilities found."]  #if not, return this message
        if result[1]: # checks if there are any recommendations found
            recommendations = result[1].split(', ')  
        else:
            recommendations = ["Keep software updated", "Restrict access via firewall"] #if not return this message
    else:
        vulnerabilities = ["No specific vulnerabilities found."]
        recommendations = ["Keep software updated", "Restrict access via firewall"]
    return vulnerabilities, recommendations

# Define a route for handling full system scan requests
@website.route('/full_scan', methods=['POST'])
def full_scan():
    input_data = request.get_json()
    ip_address = input_data.get('ipAddress', '').strip()  # gets the ip address from the form in the fullscan.html file
    

    if not ip_address: # if the IP address is empty
        return jsonify({"success": False, "error": "Please enter an IP address."}), 400     #if it is empty, return an error message
    
    else:
        print("Starting scan for", ip_address, "...") # display this message to tell user that it is working but just loading
        nm = nmap.PortScanner() 
        nm.scan(ip_address, ports='1-65000', arguments='-sT --open -T4 -Pn') #this is the nmap function that will scan for open ports on the IP address entered

        # Confirm to user that scan is done on this ip address
        print("Scan results for", ip_address)
        results = []
        if ip_address in nm.all_hosts(): # if the IP address is in the list of all hosts
            host = nm[ip_address] # get the host
            print("Host", ip_address, "has protocols:", host.all_protocols()) # display the protocols that the host has
        
            for proto in host.all_protocols():  # for each protocol that the host has
                ports = sorted(host[proto].keys()) # sort the ports that the host has
                for port in ports: # for each port that the host has
                    state = host[proto][port]['state'] # get the state of the port
                    service = host[proto][port].get('name', 'unknown') # get the service of the port
                    if state == 'open': # if the state of the port is open
                        port_info = "Port" , port , "(" , service , ") is open" # put the open port information in a good nice way to be outputted
                        vulnerabilities, recommendations = dbvulnerability(port) # get the vulnerabilities and recommendations for the port using th function made above
                        results.append({ # store all the results to the results list
                            "port_info": " ".join(map(str, port_info)),
                            "vulnerabilities": vulnerabilities,
                            "recommendations": recommendations
                        })
        else:
            print("No hosts found for", ip_address) # if the IP address is not in the list of all hosts, display this message
        return jsonify({"success": True, "results": results}), 200 # return the results of the scan from the resutls list
    

# Define a route for handling targeted system scan requests

@website.route('/targeted_scan', methods=['POST'])
def targeted_scan():
    input_data = request.get_json() # Get the user input from the form in targeted.html
    ip_address = input_data.get('ipAddress', '').strip()  # Get IP address from user input
    portt = input_data.get('ports', '').strip()  # Get the port number from user input

    if not ip_address:  # If the IP address is empty
        return jsonify({"success": False, "error": "Please enter an IP address."}), 400 # Return an error message

    if not portt.isdigit():  # check if the port is a number
        return jsonify({"success": False, "error": "Please enter a valid port number."}), 400

    port = int(portt)  # Convert to integer data type
    if port < 1 or port > 65535:  # check if the port inputted is between 1 and 65535
        return jsonify({"success": False, "error": "Port must be between 1 and 65535."}), 400 # Return an error message

    print("Starting scan for", ip_address, "on port", port, "...")  # tell user that scan started
    nm = nmap.PortScanner()
    nm.scan(ip_address, arguments=f'-p {port} -sT --open -T4 -Pn')  # perform nmap snan on the IP address and port number entered only

    print("Scan results for", ip_address, "on port", port) # tell user that scan results are ready
    results = []
    
    if ip_address in nm.all_hosts():  # Check if the IP address is in the scan results
        host = nm[ip_address]
        for proto in host.all_protocols():  # loop through all detected protocols
            if port in host[proto]:  # Check if the specified port is in scan results
                state = host[proto][port]['state']  # Get the state of the port
                service = host[proto][port].get('name', 'unknown')  # Get service name

                if state == 'open':  # If the port is open
                    port_info = f"Port {port} ({service}) is open" 
                    vulnerabilities, recommendations = dbvulnerability(port)  # Fetch vulnerabilities and recommendations
                    results.append({  # Store the results in a list in the following format
                        "port_info": port_info,
                        "vulnerabilities": vulnerabilities,
                        "recommendations": recommendations
                    })
    else:
        print("No hosts found for", ip_address) # If the IP address is not found in the scan results, display this message

    return jsonify({"success": True, "results": results}), 200  # Return scan results


if __name__ == "__main__":
    # Start the website so I can test it
    website.run(debug=True)