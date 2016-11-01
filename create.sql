CREATE TABLE Book(Isbn INTEGER PRIMARY KEY, Category TEXT, Title TEXT, Quantity INTEGER, Year INTEGER, Price REAL, PublisherId INTEGER REFERENCES Publisher(PublisherId));
CREATE TABLE Customer(CustomerId INTEGER PRIMARY KEY, Address TEXT, Name Text, Email Text);
CREATE TABLE PaymentInfo(CreditCardId INTEGER PRIMARY KEY, Type TEXT, ExpirationDate DATE, Name TEXT, CVV INTEGER);
CREATE TABLE Author(AuthorId INTEGER PRIMARY KEY, Name TEXT, Address TEXT, Phone TEXT, Email TEXT);
CREATE TABLE Publisher(PublisherId INTEGER PRIMARY KEY, Name TEXT, Address TEXT, Phone Text);
CREATE TABLE Course(CourseId INTEGER PRIMARY KEY, Professor TEXT, UniversityId TEXT, Section TEXT, Name TEXT, RequiredBook INTEGER REFERENCES Book(Isbn));
CREATE TABLE Wrote(WroteId INTEGER PRIMARY KEY AUTOINCREMENT, Isbn INTEGER REFERENCES Book(Isbn), AuthorId INTEGER REFERENCES Author(AuthorId));
CREATE TABLE Purchase(PurchaseId INTEGER PRIMARY KEY AUTOINCREMENT, CustomerId INTEGER REFERENCES Customer(CustomerId), Isbn INTEGER REFERENCES Book(Isbn), PurchaseDate DATE, PurchaseTime TIME);
CREATE TABLE CustomerPaymentInfo(CustomerPaymentInfoId INTEGER PRIMARY KEY AUTOINCREMENT, CustomerId INTEGER REFERENCES Customer(CustomerId), CreditCardId INTEGER REFERENCES PaymentInfo(CreditCardId));

