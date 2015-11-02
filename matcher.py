
from orderbook import BuyBook, SellBook
from notification import Observer

class MatchOrder(Observer):
    """Class to match the incoming buy-sell order.
    TODO: Currently the matching only happens on when a buy order comes in. This needs to
    change to also include sell orders. We should look into the buybook list for the highest matching price"""

    def deleteOrder(self, order=None, tickr=None, price=None, qty=None):
        """helper method to delete a order. Its overloaded to handle different arguments.

        :param order: incoming buy or sell order
        :type order: Order named tuple
        :param tickr: ticker name for the order
        :type tickr: str
        :param price: price of an order
        :type price: float
        :param qty: quantity of the stocks at the given price
        :type qty: int

        """
        if order:
            if order.action == 'SELL':
                sellqty = SellBook.tickrDict[order.tickr].pop(order.price)
                print "Del: Sold %d shares of %s at price %d"%(sellqty, order.tickr, order.price)
                if SellBook.tickrDict[tickr].is_empty():
                    del SellBook.tickrDict[tickr]
            else:
                BuyBook.tickrDict[order.tickr].remove((order.price,order.qty))
                print "Del: Bought %d shares of %s at price %d "%(order.qty, order.tickr, order.price)
                if not BuyBook.tickrDict[tickr]:
                    del BuyBook.tickrDict[tickr]
        if price and qty: #delete tuple from BuyBook
            BuyBook.tickrDict[tickr].remove((price,qty))
            print "Del: Bought %d shares of %s at price %d "%(qty, tickr, price)
            if not BuyBook.tickrDict[tickr]:
                del BuyBook.tickrDict[tickr]
        if price: #delete order from SellBook
            sellqty = SellBook.tickrDict[tickr].pop(price)
            print "Del: Sold %d shares of %s at price %d"%(sellqty, tickr, price)
            if SellBook.tickrDict[tickr].is_empty():
                del SellBook.tickrDict[tickr]


    def updateOrder(self, updateqty, order=None, tickr=None, price=None, qty=None ):
        """helper method to update an order. Its overloaded to handle different arguments.

        :param updateqty: number of the stocks to be subtracted from the existing number
        :type updateqty: int
        :param order: incoming buy or sell order
        :type order: Order named tuple
        :param tickr: ticker name for the order
        :type tickr: str
        :param price: price of an order
        :type price: float
        :param qty: quantity of the stocks at the given price
        :type qty: int

        """
        if order:
            if order.action == 'SELL':
                SellBook.tickrDict[order.tickr][order.price]-=updateqty
                print "Updt: Sold %d shares of %s at price %d"%\
                      (order.qty-SellBook.tickrDict[order.tickr][order.price], order.tickr, order.price)
                print "%d shares remaining of %s share at price %d"%\
                      (SellBook.tickrDict[order.tickr][order.price], order.tickr, order.price)
            else:
                BuyBook.tickrDict[order.tickr].remove((order.price,order.qty))
                BuyBook.tickrDict[order.tickr].append((order.price,order.qty-updateqty))
                print "Updt: Bought %d shares of %s at price %d"%\
                      (order.qty-BuyBook.tickrDict[order.tickr][-1][1], order.tickr, order.price)
                print "%d shares remaining of %s share at price %d"%\
                      (BuyBook.tickrDict[order.tickr][-1][1], order.tickr, order.price)

        if price and qty: #update tuple from BuyBook
            BuyBook.tickrDict[tickr].remove((price,qty))
            BuyBook.tickrDict[tickr].append((price,qty-updateqty))
            print "Updt: Bought %d shares of %s at price %d"%\
                      (qty-BuyBook.tickrDict[order.tickr][-1][1], tickr, price)
            print "%d shares remaining of %s share at price %d"%\
                      (BuyBook.tickrDict[order.tickr][-1][1], tickr, price)
            if BuyBook.tickrDict[order.tickr][-1][1] == 0:
                self.deleteOrder(tickr=tickr,price=price, qty=qty)

        if price: #update key,value from SellBook
            prevqty= SellBook.tickrDict[tickr][price]
            SellBook.tickrDict[tickr][price] -=updateqty
            print "Updt: Sold %d shares of %s at price %d"%\
                      (prevqty-SellBook.tickrDict[tickr][price], tickr, price)
            print "%d shares remaining of %s share at price %d"%\
                      (SellBook.tickrDict[tickr][price], tickr, price)
            if SellBook.tickrDict[tickr][price] == 0:
                self.deleteOrder(tickr=tickr,price=price)

    def matchOrder(self,order):
        """function to match incoming buy-sell orders
        It is called every time an order is placed. If it is a buy order then it looks for the minimum price being
        offered in the Sell Book. If the sell price happens to be less than or equal to the buy price, a transaction
        occurs for the number of stocks available at that price. The process repeats itself until the buy order is
        completely matched for the given price or if no other sell orders with a price point less than or equal to the
        quoted buy price are available.

        Drawbacks:
        -- The matching only occurs at every order placement. Which means if there are no incoming orders than
        no matching would occur even though there might be matching candidates available. Solution is to impose a timer
        mechanism that calls the method after expiration and the timer is reset if the order is placed before expiration
        -- We also need to match the incoming sell order if its quoted price is equal to or less than the available prices
        in the Buy Book. For this we will look at the highest available prices in the list

        :param order: an incoming buy or sell order
        :type order: Order named tuple

        """

        print "received quote to %s %d shares of %s at price %d"%(order.action,order.qty,order.tickr,order.price)
        print '*'*20
        SellBook.printBook()
        BuyBook.printBook()
        print '*'*20
        if order.action=='BUY':
            if order.tickr in SellBook.tickrDict:
                sell_price = SellBook.tickrDict[order.tickr].min_key()
                buy_amount= order.price*order.qty
                while sell_price <= order.price and buy_amount>0:

                    sell_qty = SellBook.tickrDict[order.tickr][sell_price]
                    sell_amount = sell_qty*sell_price
                    if sell_amount==buy_amount:
                        self.deleteOrder(order=order)
                        self.deleteOrder(tickr=order.tickr,price=order.price)
                    if sell_amount>buy_amount:
                        self.updateOrder(updateqty=sell_qty,tickr=order.tickr,price=sell_price) #update sell order
                        self.deleteOrder(order=order) #delete buy order
                    if sell_amount<buy_amount: # sell is less than buy
                        self.deleteOrder(tickr=order.tickr,price=sell_price) #delete sell order
                        self.updateOrder(updateqty=sell_qty, order=order ) #update buy order
                        if order.tickr in SellBook.tickrDict:
                            sell_price = SellBook.tickrDict[order.tickr].min_key() #update min sell price
                        else:
                            # force increase the sell price to break the loop
                            # since we cannot have any more transactions in this loop
                            sell_price = order.price+1
                            print "No more shares to sell at price %d"%order.price

                    buy_amount -= sell_amount

    def action(self,module, *args):
        """function to receive buy or sell orders from the OrderBook.

        :param module: the observed class object
        :type: SellBook class object, BuyBook class object
        """

        self.matchOrder(args[0])
