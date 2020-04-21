from django.test import TestCase

# Create your tests here.
import hashlib

mystring = input('Enter String to hash: ')

# Предположительно по умолчанию UTF-8
hash_object = hashlib.md5(mystring.encode())
print(hash_object.hexdigest())

#5d41402abc4b2a76b9719d911017c592