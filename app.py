import logging
from flask import Flask, request, jsonify
#from maindoc import generate_document

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)


''' HOOK IS CALLED WHEN API STATE CHANGES  '''
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    logging.debug("Webhook Data: %s", data)

    work_order_number = data['Object']['Id']

    if work_order_number:
        access_token = "AAEAAMfzit-vRzAcxOxXogR8T5mU6QZETDImw3Mzz0W2is3sOxzAR9fXfpuU50AWJx1VVxFCoDp2sQpCW8BJPa9KA-ZTd-XEIaO7ZJhwzONbG3aIhfNTZXN-NlGonvjJ9BeHyaLqCVNRcjfQ7v1UTLJ-HHDVbLG2R9C2HYbHEeLPmi3xPZkP15Hl2577q5RPJdNX28LaBX_W2GTVaGVRRfWcN8XPhFRGKPTrqeKOdEWi6j2EzWTvqd95OiEkSEuZzklcJqoI-jfXdw5ISs4KJgKSQXaF6VM3-TssDX-L-hL8r3ZLvQCs30oObb-e6xKqzZ44wRGozbLDuoV2Ot_lVE53l9gkAgAAAAEAADAHhvvVsJnj6I8TaVqfYlXg60F-KN8hfQ6FS5maf0nNdmE0MtSbL_oiPqLXpgqdrPa_Lbfi62Qh-GfBZ02-RThar6wpFV_TykMeZ5POHkj-FkASCcw6_Oy19z2l-VCAYdcPoXkeYGdU8TL0_0yschDL8Dqz44cT7fvAFYloUYEaQ9m_IjxGBFnsuLW1w3iZDm0XAgnB6Zjv9QgNzj6rQqZEuWa9qy5XSiDdEGuD-gwxACrxafTHRquXJV7xfG9JiQLWolkFX2eF930uwc8tY5ajehh0apc75oaxbQdZIa3nAPavJOs8aNtcQCMdK6fOynnUce6ZSxDBwMFqdHFccoU-y02UnMB5oCzNkhutvITW9USg0UAQrJt3BSxziX8ux30Kwj6MenVg_LtUavIivLz9Tr-JjYcy2hz4ZFbH57dO9cBUbo9eoZWmw80N0DvXBoQnila-KnzQ7lcueClOrIMCg_h3RfFO4Bs8lRaMvYcx5Uk0jDpkMyRKw591er5qseLG_QJKTLjh4ovMetCpyJTBnz7c3FlurjPnpx74M5v7a27gn8hFM_gh-qzhMAyXEh8ngciOa40-hTG-SoL7LtsgZWykc_b35IfwH0kFd5RWr8DuhO4FdAnm6TczBbHCDbHVDqou3MZBSS2dDgWsBODYSKUdHQJimhNAm250bedEsiaztGqqEcrdAoUOiW1nrCnoLD-KL-qAC_0FMwUMDv8"  # Replace with your actual access token
        logging.debug("Work Order Number: %s", work_order_number)

        try:
            #generate_document(work_order_number, access_token)
            return jsonify({"status": "Success", "message": "Document generated successfully"}), 200
        except Exception as e:
            logging.error("Error generating document: %s", e)
            return jsonify({"status": "Error", "message": "Failed to generate document"}), 500
    else:
        return jsonify({"status": "Error", "message": "Work order number not found in webhook data"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)