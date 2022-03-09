#!/usr/bin/env python3

import base64
import json
from vfunctions_sdk import connection
from vfunctions_sdk import NSM
from vfunctions_sdk import publish

class VFunction():
    def __init__(self):
        self.nsm = NSM.NSM()

        self.client_socket = connection.Vsock_connection()
        # Get message from the host
        print("Getting data from host")
        request_data = self.client_socket.get_message()

        print(request_data)
        self.params = request_data["params"]

        self.aws_credentials = aws_credentials
        aws_credentials = request_data["awsCredentials"]

        self.region = aws_credentials["Region"]
        self.aws_access_key_id = aws_credentials["AccessKeyId"]
        self.aws_secret_access_key = aws_credentials["SecretAccessKey"]
        self.aws_session_token = aws_credentials["SessionToken"]


    def get_attestation_doc_for_credentials(self):

        attestation_doc = self.nsm.get_attestation_doc(
            public_key=self.nsm._public_key)

        attestation_doc_b64 = base64.b64encode(attestation_doc).decode()

        return attestation_doc_b64

    def sign_results(self, data_to_sign):

        result_data = str.encode(json.dumps(data_to_sign))

        # Attestation Doc result
        attestation_doc_result = self.nsm.get_attestation_doc(user_data= result_data)
        result_attestation_doc_b64 = base64.b64encode(attestation_doc_result).decode()
        return result_attestation_doc_b64


    def decrypt(self, cipherdata):
        cipherdata = base64.b64decode(cipherdata)
        return json.loads(self.nsm.decrypt(cipherdata))


    def email_results(self, recipient, att_doc_b64):
        encoded_att_doc = str.encode(att_doc_b64)
        publish.send_email(recipient, encoded_att_doc, self.aws_credentials)


    def close(self):
        self.client_socket.close_connection()
