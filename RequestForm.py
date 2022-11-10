#in this file i'll make the request form object, along with the method for creating unique identifiers for 
#each request

#Test

#This is a test branch comment

# me making a modification to a branch 

class ProcurementRequest:

    def __init__(rnum,name,client,quant,stat,price,qObj):
        requestNum: rnum
        itemName: name
        generatedBy: client
        quantity: quant
        status: stat
        totalPrice: price
        quoteObject: qObj



def generateRequestNum():
    global reqNum
    ProcurementRequest.requestNum = reqNum
    reqNum = reqNum+1