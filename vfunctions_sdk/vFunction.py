#!/usr/bin/env python3

import base64
import json
from vfunctions_sdk import connection
from vfunctions_sdk import NSM
from vfunctions_sdk import publish

class FunctionParams():
    def __init__(self):
        self.nsm = NSM.NSM()

        self.client_socket = connection.Vsock_connection()

        # Get message from the host
        request_data = self.client_socket.get_message()

        self.params = request_data["params"]

        aws_credentials = request_data["awsCredentials"]

        self.aws_credentials = aws_credentials


    def get_attestation_doc_for_secrets(self):

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


    def email_results(self, recipient, data_to_sign):
        att_doc_b64 = self.sign_results(data_to_sign)
        encoded_att_doc = str.encode(att_doc_b64)

        publisher = publish.Publisher(self.aws_credentials)
        publisher.send_email(recipient, encoded_att_doc)

    def publish_results_to_s3(self, bucket, key, data_to_sign):
        att_doc_b64 = self.sign_results(data_to_sign)
        encoded_att_doc = str.encode(att_doc_b64)

        publisher = publish.Publisher(self.aws_credentials)
        publisher.send_email(bucket, key, encoded_att_doc)


    def close(self):
        self.client_socket.close_connection()
