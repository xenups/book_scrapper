from csv import writer


def export_book_to_csv(books):
    thecsv = writer(open("books.csv", 'a'))
    for book in books:
        thecsv.writerow([str(book.title), str(book.author), str(book.publisher)])
