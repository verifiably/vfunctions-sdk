import socket
import json
from websocket import create_connection
import boto3

class Vsock_connection():

    def __init__(self):

        self.client_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.connection_started = False

    def start_connection(self):
        # Listen for connection from any CID
        cid = socket.VMADDR_CID_ANY

        # The port should match the client running in parent EC2 instance
        client_port = 5000

        # Bind the socket to CID and port
        self.client_socket.bind((cid, client_port))

        # Listen for connection from client
        self.client_socket.listen()

        self.connection_started = True

    def get_message(self):
        if self.connection_started == False:
            self.start_connection()

        self.client_connection, addr = self.client_socket.accept()

        # Get command from client
        payload = self.client_connection.recv(4096)
        request = json.loads(payload.decode())

        return request

    
    def send(self, data):
        self.client_connection.sendall(data)

    def close_connection(self):
        self.client_connection.close()



def get_connection_id(ws):
        ws.send("hello")
        return json.loads(ws.recv())['connectionId']

def await_credentials(ws):
    value = ws.recv()
    return value


class WsockCredentialProvider:

    def __init__(self, connection_id, vFunc):
        self.connection_id = connection_id

        self.aws_credentials = vFunc.aws_credentials


    def request_credentials(self, vFunctionConnectionId, att_doc):

        client = boto3.client(
            'apigatewaymanagementapi',
            endpoint_url="https://wsock.us-east-2.verifiably.com",
            region_name = self.aws_credentials["Region"],
            aws_access_key_id = self.aws_credentials["AccessKeyId"],
            aws_secret_access_key = self.aws_credentials["SecretAccessKey"],
            aws_session_token = self.aws_credentials["SessionToken"])


        request = {
            "vFunctionConnectionId": vFunctionConnectionId,
            "att_doc": att_doc,
            "aws_credentials": self.aws_credentials
        }

        try:
            client.post_to_connection(
                Data=bytes(json.dumps(request), 'utf-8'),
                ConnectionId=self.connection_id
            )
        except Exception as e:
            print("Caught exception:")
            print(e)

    def get_credentials(self, att_doc):
        ws = create_connection("wss://wsock.us-east-2.verifiably.com")
        self.request_credentials(get_connection_id(ws), att_doc)
        return await_credentials(ws)
