import Quote
from enum import Enum
import Create_Database as db

#################################################################################################
# Class: ProcurementRequestStatus
# @members: N/A
# @methods: N/A
# 
# This class instantiates a enumeration for the status of the request.
# 
#################################################################################################
class RequestStatus(Enum):
    SENT_TO_SUPPLIER = 0
    SENT_TO_MANAGER = 1
    APPROVED = 2
    DENIED = 3

#################################################################################################
# Class: ProcurementRequest
# @members: requestNum, itemName, generatedBy, quantity, status, totalPrice, quoteObject
# @methods: getters & setters of data members
# 
# This class defines one of the main objects in the system - the procurement request.
# To generate a unique request number, the generateRequestNum() method takes a global variable
# reqNum, assigns it to the procRequest object and increments it.
#
#################################################################################################

class ProcurementRequest:
    
    database = db.Create_Database('localhost', 'root', 'star26', 'SOEN341')

    def __init__(self, rnum,name,client,quant,stat: RequestStatus, assignedManager):####include user object
        self.requestNum= rnum
        self.itemName= name
        self.generatedBy= client
        self.quantity= quant
        self.status= stat
        self.assignedManager = assignedManager

    def addRequest(self):
        self.database.add_procurement_request(self.requestNum, self.itemName, self.quantity, self.generatedBy, self.assignedManager, self.status)

    #getters
    def getRequestNum(self) -> int:
        return self.requestNum
    
    def getItemName(self) -> str:
        return self.itemName

    def getGeneratedBy(self) -> str:
        return self.generatedBy
    
    def getQuantity(self) -> int:
        return self.quantity

    def getStatus(self) -> RequestStatus:
        return self.status

    #setters
    def setRequestNum(self):
        i = i.generateRequestNum()
        self.requestNum = i

    def setItemName(self, itemName):
        self.itemName = itemName

    def setGeneratedBy(self,generatedBy):
        self.generatedBy = generatedBy

    def setQuantity(self,quantity):
        self.quantity = quantity

    def setStatus(self, status:RequestStatus):
        self.status = status

    def setManager(self, manager):
        self.assignedManager = manager


