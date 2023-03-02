import json

class Address:
    def __init__(self, street, city, state, zip):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

class PhoneNumber:
    def __init__(self, type, number):
        self.type = type
        self.number = number

class Person:
    def __init__(self, name, age, email, address, phone_numbers):
        self.name = name
        self.age = age
        self.email = email
        self.address = address
        self.phone_numbers = phone_numbers

    def get(self, key):
            return getattr(self, key, None)

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        address_data = data['address']
        address = Address(
            address_data['street'],
            address_data['city'],
            address_data['state'],
            address_data['zip']
        )
        phone_numbers_data = data['phone_numbers']
        phone_numbers = [
            PhoneNumber(pn['type'], pn['number'])
            for pn in phone_numbers_data
        ]
        return cls(
            data['name'],
            data['age'],
            data['email'],
            address,
            phone_numbers
        )

# Open the JSON file and read its contents
with open('data.json') as f:
    json_string = f.read()

# Parse the JSON string into a Person object
person = Person.from_json(json_string)

# Access the data in the Person object
print(person.name)
print(person.age)
print(person.email)
print(person.address.street)
print(person.address.city)
print(person.address.state)
print(person.address.zip)
for phone_number in person.phone_numbers:
    print(phone_number.type, phone_number.number)
