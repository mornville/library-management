from django.db import models

"""


Fulfil a books reservation when the book is return


- Make return_book
    - increase the count by 1
    - remove the book from Member class
    - check if there are any reservations for this book_id
    - If yes, Check the members list and get the first one
    - Make a relation with Member and the Book
    
    
    """

class Books(models.Model):
    def __str__(self) -> str:
        return f"{self.book_name} - {self.book_id}"
    book_id = models.CharField(max_length=20, unique=True)
    book_name = models.CharField(max_length=1000)
    no_of_copies = models.IntegerField()


class Members(models.Model):
    def __str__(self) -> str:
        return f"{self.member_name} - {self.mem_id}"
    
    mem_id = models.CharField(unique=True)
    member_name = models.CharField(max_length=100)
    books_taken = models.ManyToManyField(Books, related_name="member_books", default=[])    

        
class Reservation(models.Model):
    def __str__(self) -> str:
        return f"Book - {self.book}; Members = {self.members.all()}"
    
    book = models.ForeignKey(Books, related_name="book_reservations", on_delete=models.PROTECT, unique=True)
    members = models.ManyToManyField(Members, related_name="member_reservations", null=True)
    
    
            