import csv
import sys
from random import randint
from faker import Factory
fake = Factory.create()

class Book:
	"""docstring for Book"""
	def __init__(self):
		self.isbn  = 0
		self.title = 0
		self.authors = []
		self.publisher = ''
		self.year = 0
		self.price = 0
		self.category = ''

file = sys.argv[1]
output = open('out.sql', 'w')

books = []

with open(file, 'r') as f:
	next(f)
	reader = csv.reader(f)
	curBook = None
	for row in reader:
		if row[0]:
			book = Book()
			book.isbn = row[0]
			book.title = row[1]
			book.authors.append(row[2])
			book.publisher = row[3]
			book.year = row[4]
			book.price = row[5]
			book.category = row[6]
			curBook = book
			books.append(curBook)
		else:
			curBook.authors.append(row[2])

# Create publishers
# CREATE TABLE Publisher(PublisherId INTEGER PRIMARY KEY, Name TEXT, Address TEXT, Phone TEXT);
publishers = sorted(list(set([book.publisher for book in books])))
publisher_dict = {}
publisher_template = "INSERT INTO Publisher VALUES(%d, \"%s\", \"%s\", \"%s\");"
for i in range(len(publishers)):
	output.write(publisher_template % (i + 1, publishers[i], fake.address().replace('\n', ' '), fake.phone_number()))
	output.write('\n')
	publisher_dict[publishers[i]] = i + 1

output.write('\n')

# Create authors
# CREATE TABLE Author(AuthorId INTEGER PRIMARY KEY, Name TEXT, Address TEXT, Phone TEXT, Email TEXT);
authors = sorted(list(set([author for book in books for author in book.authors])))
author_dict = {}
author_template = "INSERT INTO Author VALUES(%d, \"%s\", \"%s\", \"%s\", \"%s\");"
for i in range(len(authors)):
	output.write(author_template % (i + 1, authors[i].decode('ascii', 'ignore'), fake.address().replace('\n', ' '), fake.phone_number(), fake.safe_email()))
	output.write('\n')
	author_dict[authors[i]] = i + 1

output.write('\n')

# Create books
# CREATE TABLE Book(Isbn INTEGER PRIMARY KEY, Category TEXT, Title TEXT, Quantity INTEGER, Year INTEGER, Price REAL, PublisherId INTEGER REFERENCES Publisher(PublisherId));
book_dict = {}
book_template = "INSERT INTO Book VALUES(%d, \"%s\", \"%s\", %d, %d, %f, %d)"
for book in books:
	output.write(book_template % (int(book.isbn), book.category, book.title, randint(0, 500), int(book.year), float(book.price.replace('$', '')), publisher_dict[book.publisher]))
	output.write('\n')
	book_dict[book.isbn] = book

output.close()
