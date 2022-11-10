#################################################################################################
# Class: ProcurementRequest
# @members: requestNum, itemName, generatedBy, quantity, status, totalPrice, quoteObject
# @methods: generateRequestNum()
# 
# This class defines one of the main objects in the system - the procurement request.
# To generate a unique request number, the generateRequestNum() method takes a global variable
# reqNum, assigns it to the procRequest object and increments it.
#
#################################################################################################


#in this file i'll make the request form object, along with the method for creating unique identifiers for 
#each request
import Quote

class ProcurementRequest:

    def __init__(self, rnum,name,client,quant,stat,price,qObj):
        self.requestNum= rnum
        self.itemName= name
        self.generatedBy= client
        self.quantity= quant
        self.status= stat
        self.totalPrice= price
        self.quoteObject= qObj

    #generates & the request number
    def generateRequestNum() -> int:
        global reqNum
        reqNum = reqNum+1
        return reqNum


    #getters
    def getRequestNum(self) -> int:
        return self.requestNum
    
    def getItemName(self) -> str:
        return self.itemName

    def getGeneratedBy(self) -> str:
        return self.generatedBy
    
    def getQuantity(self) -> int:
        return self.quantity

    def getStatus(self) -> str:
        return self.status

    def getTotalPrice(self) -> float:
        return self.totalPrice

    def getQuoteObject(self) -> Quote:
        return self.quoteObject

    #setters
    def setRequestNum(self):
        i = i.generateRequestNum()
        self.requestNum = i

    def setItemName(self, n):
        self.itemName = n

    def setGeneratedBy(self,g):
        self.generatedBy = g

    def setQuantity(self,q):
        self.quantity = q

    def setStatus(self, s):
        self.status = s

    def setTotalPrice(self, p):
        self.totalPrice = p

    def setQuoteObject(self, q):
        self.quoteObject = q

    
    