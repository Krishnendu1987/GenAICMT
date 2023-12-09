import uuid
def processMedHCP(refundRequest):
    #Medicine Processing
    diseaseName = refundRequest['diseaseName']
    medID = uuid.uuid4()
    return f"Refund For {diseaseName} processed successfully. Refund Reference {medID}"

def processMovieAnalyst(returnRequest):
    movieName = returnRequest['movieName']
    movieID = uuid.uuid4()
    return f"Return For {movieName} initiated successfully. Return Reference {movieID}"
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