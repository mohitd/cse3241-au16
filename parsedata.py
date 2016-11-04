import csv
import sys
import string
from random import randint, choice
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

file = 'proj-data.csv'
output = open('create.sql', 'w')

books = []

output.write("PRAGMA foreign_keys=ON;\n")
output.write("CREATE TABLE Book(Isbn INTEGER PRIMARY KEY, Category TEXT, Title TEXT, Quantity INTEGER, Year INTEGER, Price REAL, PublisherId INTEGER REFERENCES Publisher(PublisherId));\n")
output.write("CREATE TABLE Customer(CustomerId INTEGER PRIMARY KEY, Name TEXT, Address TEXT, Email TEXT);\n")
output.write("CREATE TABLE PaymentInfo(CreditCardId INTEGER PRIMARY KEY, Type TEXT, ExpirationDate TEXT, Name TEXT, CVV INTEGER);\n")
output.write("CREATE TABLE Author(AuthorId INTEGER PRIMARY KEY, Name TEXT, Address TEXT, Phone TEXT, Email TEXT);\n")
output.write("CREATE TABLE Publisher(PublisherId INTEGER PRIMARY KEY, Name TEXT, Address TEXT, Phone TEXT);\n")
output.write("CREATE TABLE Course(CourseId INTEGER PRIMARY KEY, Professor TEXT, UniversityId TEXT, Section TEXT, Name TEXT, RequiredBook INTEGER REFERENCES Book(Isbn));\n")
output.write("CREATE TABLE Wrote(WroteId INTEGER PRIMARY KEY AUTOINCREMENT, Isbn INTEGER REFERENCES Book(Isbn), AuthorId INTEGER REFERENCES Author(AuthorId));\n")
output.write("CREATE TABLE Purchase(PurchaseId INTEGER PRIMARY KEY AUTOINCREMENT, CustomerId INTEGER REFERENCES Customer(CustomerId), Isbn INTEGER REFERENCES Book(Isbn), PurchaseDate TEXT, PurchaseTime TEXT);\n")
output.write("CREATE TABLE CustomerPaymentInfo(CustomerPaymentInfoId INTEGER PRIMARY KEY AUTOINCREMENT, CustomerId INTEGER REFERENCES Customer(CustomerId), CreditCardId INTEGER REFERENCES PaymentInfo(CreditCardId));\n")
output.write('\n')

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
for i in xrange(len(publishers)):
	output.write(publisher_template % (i + 1, publishers[i], fake.address().replace('\n', ' '), fake.phone_number()))
	output.write('\n')
	publisher_dict[publishers[i]] = i + 1

output.write('\n')

# Create authors
# CREATE TABLE Author(AuthorId INTEGER PRIMARY KEY, Name TEXT, Address TEXT, Phone TEXT, Email TEXT);
authors = sorted(list(set([author for book in books for author in book.authors])))
author_dict = {}
author_template = "INSERT INTO Author VALUES(%d, \"%s\", \"%s\", \"%s\", \"%s\");"
for i in xrange(len(authors)):
	output.write(author_template % (i + 1, authors[i].decode('ascii', 'ignore'), fake.address().replace('\n', ' '), fake.phone_number(), fake.safe_email()))
	output.write('\n')
	author_dict[authors[i].decode('ascii', 'ignore')] = i + 1

output.write('\n')

# Create books
# CREATE TABLE Book(Isbn INTEGER PRIMARY KEY, Category TEXT, Title TEXT, Quantity INTEGER, Year INTEGER, Price REAL, PublisherId INTEGER REFERENCES Publisher(PublisherId));
book_dict = {}
book_template = "INSERT INTO Book VALUES(%d, \"%s\", \"%s\", %d, %d, %f, %d);"
for book in books:
	output.write(book_template % (int(book.isbn), book.category, book.title, randint(0, 500), int(book.year), float(book.price.replace('$', '')), publisher_dict[book.publisher]))
	output.write('\n')
	book_dict[int(book.isbn)] = book

output.write('\n')

# CREATE TABLE Customer(CustomerId INTEGER PRIMARY KEY, Name TEXT, Address TEXT, Email TEXT);
customer_template = "INSERT INTO Customer VALUES(%d, \"%s\", \"%s\", \"%s\");"
for i in xrange(1, 21):
	output.write(customer_template % (i, fake.name(), fake.address().replace('\n', ' '), fake.safe_email()))
	output.write('\n')

output.write('\n')

# CREATE TABLE PaymentInfo(CreditCardId INTEGER PRIMARY KEY, Type TEXT, ExpirationDate TEXT, Name TEXT, CVV INTEGER);
cc_nums = []
payment_info_template = "INSERT INTO PaymentInfo VALUES(%d, \"%s\", \"%s\", \"%s\", %d);"
for i in xrange(1, 21):
	cc = int(fake.credit_card_number(card_type=None))
	cc_nums.append(cc)
	output.write(payment_info_template % (cc, choice(['Mastercard', 'Visa', 'Discover']), fake.date(pattern="%m-%d"), fake.name(), randint(100, 999)))
	output.write('\n')

output.write('\n')

# CREATE TABLE Course(CourseId INTEGER PRIMARY KEY, Professor TEXT, UniversityId TEXT, Section TEXT, Name TEXT, RequiredBook INTEGER REFERENCES Book(Isbn));
course_names = ['ENGR 1281.02H', 'MATH 2162.02H', 'ENGR 1100.06', 'PSYCH 1100', 'MATH 2568', 'STAT 3470', 'CSE 2221', 'SOCIOL 3302', 'CSE 2231', 'CSE 2321', 'MATH 3345', 'ECE 2000', 'CSE 2331', 'CSE 2421', 'ECE 2100', 'CSE 2431', 'CSE 3902', 'COMPSTD 1100', 'CSE 3241', 'CSE 5526']
course_template = "INSERT INTO Course VALUES(%d, \"%s\", \"%s\", \"%s\", \"%s\", %d);"
for i in xrange(1, 21):
	unid = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(10))
	section = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(10))
	output.write(course_template % (i, fake.name(), unid, section, course_names[i-1], choice(book_dict.keys())))
	output.write('\n')

output.write('\n')

# CREATE TABLE Wrote(WroteId INTEGER PRIMARY KEY AUTOINCREMENT, Isbn INTEGER REFERENCES Book(Isbn), AuthorId INTEGER REFERENCES Author(AuthorId));
wrote_template = "INSERT INTO Wrote(Isbn, AuthorId) VALUES(%d, %d);"
for book in books:
	for author in book.authors:
		output.write(wrote_template % (int(book.isbn), int(author_dict[author.decode('ascii', 'ignore')])))
		output.write('\n')

output.write('\n')

# CREATE TABLE Purchase(PurchaseId INTEGER PRIMARY KEY AUTOINCREMENT, CustomerId INTEGER REFERENCES Customer(CustomerId), Isbn INTEGER REFERENCES Book(Isbn), PurchaseDate TEXT, PurchaseTime TEXT);
purchase_template = "INSERT INTO Purchase(CustomerId, Isbn, PurchaseDate, PurchaseTime) VALUES(%d, %d, \"%s\", \"%s\");"
for i in xrange(1, 21):
	output.write(purchase_template % (choice(xrange(1, 21)), int(choice(book_dict.keys())), fake.date(pattern="%Y-%m-%d"), fake.time(pattern="%H:%M:%S")))
	output.write('\n')

output.write('\n')

# CREATE TABLE CustomerPaymentInfo(CustomerPaymentInfoId INTEGER PRIMARY KEY AUTOINCREMENT, CustomerId INTEGER REFERENCES Customer(CustomerId), CreditCardId INTEGER REFERENCES PaymentInfo(CreditCardId));
customer_payment_template = "INSERT INTO CustomerPaymentInfo(CustomerId, CreditCardId) VALUES(%d, %d);"
for i in xrange(1, 21):
	output.write(customer_payment_template % (choice(xrange(1, 21)), cc_nums[i-1]))
	output.write('\n')

output.close()
