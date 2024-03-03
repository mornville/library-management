import json
from django.http import HttpResponse
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from book_management.models import *
from loguru import logger

"""
Scenario not handled: Ordering in the queue of members"""


""""
FINE - Book not returned for more than 7 days
"""

def return_book(request):
    """
    View to return  a book
    - Expects:
        - book_id
        - member_id
    1. checks validation of the input
    2. if book is found, increase the number of copies of the book
    3. Remove books_taken from the Member
    4. Check if the current book has any reservation queues
    5. If yes; get the last memnber a
    5.1 assign the books_taken; decrease the count; remove from queue
    """
    if request.method == "GET":
        return HttpResponse(status=HTTP_404_NOT_FOUND)

    # Post
    try:
        input_data = json.loads(request.body.decode("utf-8"))

        book_id = input_data.get("book_id", None)
        member_id = input_data.get("member_id", None)

        logger.debug(f"Input: {input_data}")
        if not member_id or not book_id:
            return HttpResponse({"Incorrect data"}, status=HTTP_400_BAD_REQUEST)

        requesting_member: Members = Members.objects.get(mem_id=member_id)
        logger.info(f"Requesting Member: {requesting_member}")
        requested_book = requesting_member.books_taken.get(book_id=book_id)

        logger.debug(
            f"Processing request for RETURN {requested_book.book_name=}; {requesting_member.member_name=}"
        )

        # Remove the book from
        requesting_member.books_taken.remove(requested_book)
        requesting_member.save()

        # increase the count of the requested_book
        requested_book.no_of_copies += 1
        requested_book.save()

        logger.info("Book returned succesfully; Checking for Queue")

        res_queue = Reservation.objects.filter(book=requested_book).first()

        if res_queue:
            # Queue found. Assign and decrease the number
            member_to_be_assigned = list(res_queue.members.all())[-1]

            logger.info(f"Assigning Book to {member_to_be_assigned}")
            requested_book.no_of_copies -= 1
            member_to_be_assigned.books_taken.add(requested_book)
            member_to_be_assigned.save()
            requested_book.save()

            return HttpResponse(
                {f"Return succesful with giving book to {member_to_be_assigned=}"},
                status=200,
            )

        return HttpResponse(
            {f"Return succesful with giving book to {requesting_member=}"},
            status=200,
        )

    except (Books.DoesNotExist, Members.DoesNotExist) as exc:
        return HttpResponse(
            {f"Incorrect data, could find data in DB; {exc}"}, HTTP_400_BAD_REQUEST
        )

    except Exception as exc:
        logger.error(f"Error checking out: {repr(exc)}")
        return HttpResponse({f"Error checking out: {repr(exc)}"}, 500)


def checkout_book(request):
    """
    View to check out a book
    - Expects:
        - book_id
        - member_id
    """
    if request.method == "GET":
        return HttpResponse(status=HTTP_404_NOT_FOUND)

    # Post
    try:
        input_data = json.loads(request.body.decode("utf-8"))

        book_id = input_data.get("book_id", None)
        member_id = input_data.get("member_id", None)

        logger.debug(f"Input: {input_data}")
        if not member_id or not book_id:
            return HttpResponse({"Incorrect data"}, status=HTTP_400_BAD_REQUEST)

        requested_book: Books = Books.objects.get(book_id=book_id)
        requesting_member: Members = Members.objects.get(mem_id=member_id)

        logger.debug(
            f"Processing request for {requested_book.book_name=}; {requesting_member.member_name=}"
        )

        no_copies = requested_book.no_of_copies

        logger.error(no_copies)
        # If books exist
        if no_copies >= 1:
            logger.debug(f"Found more than 0 copies {no_copies=}, checking out")
            requested_book.no_of_copies -= 1
            requesting_member.books_taken.add(requested_book)
            requested_book.save()
            requesting_member.save()

            return HttpResponse({"Checkout succesful"}, status=200)

        # If not
        # if less than 1
        # Reserve a book and move to reservation queue when a particular book has no copies available in case of a ‘checkout’ request.
        else:
            logger.debug(f"Book not availale with current {no_copies=}, RESERVING")

            # Get the res_queue; Create reservation queue
            _ = Reservation.objects.get_or_create(book=requested_book)
            res_queue = Reservation.objects.get(book=requested_book)
            res_queue.members.add(requesting_member)

            res_queue.save()

            logger.debug(f"Updated queue = {res_queue=}")
            return HttpResponse(
                {f"Updating Reservation by RESERVATION; {res_queue=}"}, status=200
            )
    except (Books.DoesNotExist, Members.DoesNotExist):
        return HttpResponse(
            {"Incorrect data, could find data in DB"}, HTTP_400_BAD_REQUEST
        )

    except Exception as exc:
        logger.error(f"Error checking out: {repr(exc)}")

        return HttpResponse({"Error checking out: {repr(exc)}"}, 500)


def add_books(request):
    """
    API to add books to database
    """
    if request.method == "GET":
        return HttpResponse(status=HTTP_404_NOT_FOUND)

    # for POST
    input_data = json.loads(request.body.decode("utf-8"))
    books_data = input_data
    logger.error(input_data)

    for _, book in enumerate(books_data):
        book_name, book_id, book_copies = (
            book.get("name", None),
            book.get("id"),
            book.get("copies"),
        )

        if not book_name or not book_copies or not book_id:
            return HttpResponse(status=HTTP_400_BAD_REQUEST)

        # Create data in case of correct input
        Books.objects.create(
            book_name=book_name, book_id=book_id, no_of_copies=book_copies
        )

    return HttpResponse({}, status=200)


def add_members(request):
    """
    API to add members to database
    """
    if request.method == "GET":
        return HttpResponse(status=HTTP_404_NOT_FOUND)

    for i in range(0, 21):
        Members.objects.create(
            member_name=f"Member {i+1}",
            mem_id=f"{2000 + i}",
        )

    return HttpResponse({}, status=200)
