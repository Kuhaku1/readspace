# from django.test import TestCase

# Create your tests here.
from .models import Book, BookRanking, Press, Family, Subsection


def testsclearrank():
    book = Book.userManager.all()
    for tmp in book:
        aa = BookRanking.object.filter(book=tmp).first()
        if not aa:
            BookRanking.userManager.createranking(tmp)
        else:
            BookRanking.userManager.clearRanking(aa)
