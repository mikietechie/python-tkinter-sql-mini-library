'''
By Mike Zinyoni

25 November 2021

+263713122648
mzinyoni7@outlook.com
looking for a job ASAP
'''
from db import Book
import os
from pprint import pprint


def clear(): os.system("cls")

def get_validated_input(q, _type="str", min_len=1, max_len=111):
    input_val = input(q)
    if input_val.__len__() < min_len or input_val.__len__() > max_len:
        print("!!!invalid length!!!")
        return get_validated_input(q, _type, min_len, max_len)
    if _type == "int" and not input_val.isdigit():
        print(f"!!!invalid datatype, we need integer!!!")
        return get_validated_input(q, _type, min_len, max_len)
    return int(input_val) if _type == "int" else input_val
        

print("*** Welcome to Mini Library ***\n\n\n")

def menu(option):
    clear()
    if option == "1":
        print("*** All Books *** \n\n")
        Book.table(Book.all())
    elif option == "2":
        print("*** Filter ***\n\n")
        books = Book.filter(
            column=input("Enter filter column from [title, author, year, publisher, id]\t:\n"),
            query_val=input("Enter filter value\t:\n"))
        Book.table(books)
    elif option == "3":
        print("*** Get one by id ***\n\n")
        book = Book.get(query_val=get_validated_input("Enter book id\t:\n", "int"))
        if book:
            pprint(book.__dict__)
        else:
            print("Book not found...")
    elif option == "4":
        print("*** Create book ***\n\n")
        while True:
            if Book(
                title = get_validated_input("Please enter title\t:\n", "str", 1, 128),
                author = get_validated_input("Please enter author\t:\n", "str", 1, 128),
                year = get_validated_input("Please enter year\t:\n", "int", 4, 4),
                publisher = get_validated_input("Please enter publisher\t:\n", "str",1, 128 )
                ).save():
                print("***Saved***")
                break
            else: print("An error occured try again...")
    elif option == "5":
        print("*** Update book ***\n\n")
        print("*** Get one by id ***\n\n")
        book = Book.get(query_val=get_validated_input("Enter book id\t:\n", "int"))
        if book:
            pprint(book.__dict__)
            while True:
                if Book(
                    title = get_validated_input("Please enter title\t:\n", "str", 1, 128),
                    author = get_validated_input("Please enter author\t:\n", "str", 1, 128),
                    year = get_validated_input("Please enter year\t:\n", "int", 4, 4),
                    publisher = get_validated_input("Please enter publisher\t:\n", "str",1, 128),
                    id = book.id
                    ).save():
                    print("***Updated***")
                    break
                else: print("An error occured try again...")
        else:
            print("Book not found...")
    elif option == "6":
        print("*** Delete book ***\n\n")
        print("*** Get one by id ***\n\n")
        book = Book.get(query_val=get_validated_input("Enter book id\t:\n", "int"))
        if book:
            if input(f"Are you sure you want to delete {book}?\t: y\\n\n").lower() == "y":
                book.delete()
                print("book deleted")
        else:
            print("Book not found...")
    else:
        print("***Option selected is invalid***")
def done(msg=""):
    print((msg or "\nDone!"))
    option = input("""Select Option\n1) Main\n2)Exit\n""")
    if option == "1":
        clear()
        main()
    else:
        print("***Exiting***")
        exit()

def main():
    print("\n*** MENU ***\n")
    option = input("""
        1) List All\n
        2) Filter \n
        3) Get one\n
        4) Create one\n
        5) Update one\n
        6) Delete one\n\n""")
    menu(option)
    done()


if __name__ == '__main__':
    main()
    



