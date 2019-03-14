import os

print(os.path.join(os.path.dirname(os.path.dirname(__file__)),'images'))
print(os.path.join(os.getcwd(),'images'))

print(os.path.exists('../bmw'))
print(os.path.exists('spiders'))