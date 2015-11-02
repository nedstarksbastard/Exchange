__author__ = 'fizi'


from orderbook import SellBook, BuyBook
from orderstream import OrderStream
from matcher import MatchOrder


def main():
    ostream = OrderStream() #instantiate the stream of orders
    sellbook = SellBook(ostream) #instantiate the dict that will handle sell orders. make it an observer of the stream
    buybook = BuyBook(ostream)#instantiate the dict that will handle buy orders. make it an observer of the stream
    m = MatchOrder(sellbook,buybook)#instantiate matching. make it an observer of buybook and sellbook

    for i in range(5):
        ostream.sendorder()

    #m.printBook()
    #print '*'*20
    #m.printBook()

if __name__ == "__main__":
    main()