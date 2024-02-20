from flask import Flask, request, jsonify
from azure.communication.email import EmailClient
from azure.core.credentials import AzureKeyCredential
import base64
import mimetypes
app = Flask(__name__)

def send_email(message):
    credential = AzureKeyCredential("iW6Yig90/QSax5Qy9wwyjtTHQB8rO3+h2iBLbKOMUNW+/JdjxP77OMgTZh9O7gydsOAMnCxOfDktVz+hFYv/nA==")
    endpoint = "https://pre-hpe-itg-cs.europe.communication.azure.com"
    client = EmailClient(endpoint, credential)

    poller = EmailClient.begin_send(client, message)
    result = poller.result()
    return result

@app.route('/send_email', methods=['POST'])
def send_email_api():
    try:
        data = request.get_json()
        Recipient_Email_Address = data.get("Recipient_emails")
        attachment_paths = data.get("attachments", [])

        attachment_list = []
        for attachment_base64 in attachment_paths:
            attachment_list.append({
                "name": "attachment.zip",  # You can customize the attachment name if needed
                "contentType": "application/zip",
                "contentInBase64": attachment_base64
            })

        message = {
            "content": {
                "subject": "Test Mail",
                "plainText": "The body of the email",
            },
            "recipients": {
                "to": [
                            {"address": email} for email in Recipient_Email_Address.split(",")
                ]
            },
            "senderAddress": "DoNotReply@vsa.ext.hpe.com",
            "attachments": attachment_list
        }

        result = send_email(message)
        return jsonify({"status": "Email sent successfully", "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
