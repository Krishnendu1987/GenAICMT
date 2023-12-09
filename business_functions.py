import uuid
def processRefund(refundRequest):
    #Refund Processing
    orderNumber = refundRequest['orderNumber']
    refundID = uuid.uuid4()
    return f"Refund For {orderNumber} processed successfully. Refund Reference {refundID}"

def processReturn(returnRequest):
    orderNumber = returnRequest['orderNumber']
    returnID = uuid.uuid4()
    return f"Return For {orderNumber} initiated successfully. Return Reference {returnID}"
nofunctionsArr = []
functionsArr = [
        {
            "name": "processMedHCP",
            "description": "Prescrib medicine for a disease",
            "parameters": {
                "type": "object",
                "properties": {
                    "diseaseName": {
                        "type": "string",
                        "description": "Name of the disease"
                    },
                    "patientname": {
                        "type": "string",
                        "description": "Name of the patient"
                    }

                },
                "required": ["diseaseName", "patientname"]
            },


        },
        {
            "name": "processMovieAnalyst",
            "description": "Purchase Movie Ticket",
            "parameters": {
                "type": "object",
                "properties": {
                    "movieName": {
                        "type": "string",
                        "description": "Name of the Movie"
                    },
                    "customername": {
                        "type": "string",
                        "description": "Name of the customer"
                    }

                },
                "required": ["movieName", "customername"]
            },

        },

    ]