
# implementing the class that will handle the quote (i.e price of each item)

import Users

class Quote:

        # constructor 

        def __init__(self,Price, supplier):
                 self.Price = Price 
                 self.user = supplier

        # getter and setter
        def GetPrice(self,Price) -> float:
                return self.Price

        def SetPrice(self, p) -> str:
                self.Price = p
        


    











