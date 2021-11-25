import sqlite3


connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INT NOT NULL UNIQUE,
        title VARCHAR(128) NOT NULL,
        author VARCHAR(128) NOT NULL,
        year INT NOT NULL,
        PUBLISHER VARCHAR(128) NOT NULL,
        PRIMARY KEY(id, 'AUTOINCREMENT')
    )
""")

class Book(object):
    def __init__(self, title, author, year, publisher, id=0):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.publisher = publisher
    
    @classmethod
    def max_id(cls):
        try:
            return cursor.execute("SELECT MAX(id) FROM books").fetchone()[0]
        except: return 0
    
    @classmethod
    def bookfy(cls, book_row):
        return Book(book_row[1], book_row[2], book_row[3], book_row[4], book_row[0])
        
    @classmethod
    def get(cls, query_val):
        try:
            query = "SELECT * FROM books WHERE " + (f"title='{query_val}'" if isinstance(query_val, str) else f"id={query_val}")
            return cls.bookfy(cursor.execute(query).fetchone())
        except:
            return None
        
    @classmethod
    def table(cls, book_list):
        print(cls.table_head())
        for book in book_list:
            print(book.table_row)
        
    @classmethod
    def filter(cls, column, query_val: str):
        try:
            qv = int(query_val) if query_val.isdigit() else f"'{query_val}'"
            query = f"SELECT * FROM books WHERE {column}={qv}"
            return [cls.bookfy(book_row) for book_row in cursor.execute(query).fetchall()]
        except:
            return []
        
        
    @classmethod
    def clear(cls):
        cursor.execute("DELETE FROM books")
        connection.commit()
        return True
    
    @classmethod
    def all(cls):
        return [cls.bookfy(book) for book in cursor.execute("SELECT * FROM books").fetchall()]
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    @property
    def table_row(self):
        return f"{str(self.id):4} {str(self.title):20} {str(self.author):20} {str(self.year):4} {str(self.publisher):10}"
    
    @classmethod
    def table_head(cls):
        return f"{str('id'):4} {str('title'):20} {str('author'):20} {str('year'):4} {str('publisher'):10}"
    
    def save(self):
        if self.id:
            try:
                cursor.execute(f"UPDATE books SET title='{self.title}', author='{self.author}', year={self.year}, publisher='{self.publisher}' WHERE  id={self.id}")
            except Exception as e:
                print(e)
                return None
        else:
            try:
                cursor.execute(f"INSERT INTO books (title, author, year, publisher, id) VALUES ('{self.title}', '{self.author}', {self.year}, '{self.publisher}', {self.max_id()+1})")
            except Exception as e:
                print(e)
                return None
        connection.commit()
        return True

    def delete(self):
        try:
            cursor.execute(f"DELETE FROM books WHERE id={self.id}")
            connection.commit()
            return True
        except Exception as e:
            print(e)
            return None
        
    def __iter__(self):
        return iter([val for val in self.__dict__.values()])

if not len(Book.all()):
    # Logic to populate database
    for book_row in [
            (None, 'snatch', 'guy ritchie', 1999, 'mhs'),
            (None, 'lock, stock n barrel', 'guy ritchie', 1958, 'mhs'),
            (None, 'tokyo drift', 'justin lin', 1976, 'wpa'),
            (None, 'the hateful ', 'quentin tarrantino', 1988, 'mhs'),
            (None, 'expandables', 'sylvestor stallon', 1988, 'mhs'),
            (None, 'tha passion of the christ', 'mel gibson', 1988, 'wb')
        ]:
        Book.bookfy(book_row).save()

connection.commit()
