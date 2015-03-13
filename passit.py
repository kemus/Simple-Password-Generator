#!/usr/bin/python
from getpass import getpass
from string import ascii_letters, digits, punctuation
from os.path import expanduser
from hashlib import new
alg = "sha512"
password = None
verified = None
length = 8
numpass = 0
numletters = 0
start={}
end={}
hsave={}
template = "%4s: %4s | %5s | %4s | %s"
# prints a line of length 'width'
def line(width):
    print('\n' + '-'*width + '\n')

print("pashash v1.0")
charset = ascii_letters + digits + punctuation

numchars = len(charset)
line(25)
print("%d characters in charset: "%numchars)
for i in range(0,numchars,25):
    print(charset[i:i+25])
line(25)

while password is None or password != verified:
    password = getpass('\nmaster password: ')
    verified = getpass('repeat password: ')
service  = input('\nfor service: ')
username = input('on username: ')

line(33)
print("""generating passwords for service: %s
                     on username: %s"""%(service, username))

sources = password, service, username
line(33)

numbers = []
for source in sources:
    source = source.encode('utf8')
    hashed = new(alg,source).digest()
    hsave[source]=hashed
    numbers.extend([int(byte) for byte in hashed])
letters = [charset[number%numchars] for number in numbers]
letters = ''.join(letters)
numletters = len(letters)

print("generated passwords using %s"%alg)
line(33)
print(template%("num", "len", "start", "end", "password"))
numletters = 0
for length in range(8,21,4):
    for i in range(3):
        numpass += 1
        password= letters[0:length]
        letters = letters[length:]
        start[numpass] = numletters
        print(template%(str(numpass),
                        str(len(password)),
                        str(numletters),
                        str(numletters+len(password)),
                        password))
        numletters += len(password)
        end[numpass] = numletters

saved = None
try:
    saved = int(input('pick a number to save, or anything else to just exit'))
    print(saved, numpass)
    if saved < 1 or saved > numpass:
        raise Exception
    else:
        p = expanduser('~/.pashash/%s-%s.py'%(service,username))
        print("attempting to save to %s"%p)
        with open(p,'w+') as f:
            f.write('''\
#!/usr/bin/python
from hashlib import *
from getpass import getpass
print(''.join(["""%s"""[int(c)%%%d] \
          for c in b''.join([%s(s.encode("utf8")).digest() \
              for s in ((getpass("password: ")), "%s","%s") ])])[%d:%d])\
'''%(
     charset,
     numchars,
     alg,
     service,
     username,
     start[saved],
     end[saved]))
except Exception as E:
    print(E)
    print("not saving password...")
    pass


