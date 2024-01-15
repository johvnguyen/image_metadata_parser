from JPGParser.JPGParser import JPGParser

filename = 'profile.jpg'
filepath = ''.join(['./images/jpg/', filename])

parser = JPGParser()
parser.parse(filepath)
