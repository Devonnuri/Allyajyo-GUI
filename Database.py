import sys


class Database:
    # Class Database: Database that can store string value in a text file
    # Database(filename) : Construct database class and, set 'filename' to database file
    # Database.add(item) : Add 'item' into database
    # Databaes.delete(item) : Delete 'item' into database

    def __init__(self, filename):
        self.filename = filename

    def add(self, data):
        try:
            db_file = open(self.filename, "a")
        except IOError:
            sys.exit()
        db_file.write(data + "\n")
        db_file.close()

    def delete(self, data):
        try:
            db_file = open(self.filename, 'r')
        except IOError:
            sys.exit()
        db_list = db_file.readlines()
        db_file.close()

        try:
            db_file = open(self.filename, "w")
        except IOError:
            sys.exit()

        for item in db_list:
            item = item.strip('\n')
            if item == data:
                continue
            db_file.write(item + "\n")
        db_file.close()