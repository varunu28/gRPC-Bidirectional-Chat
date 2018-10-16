import threading
import grpc
import sys
import time
import messenger_pb2
import messenger_pb2_grpc

import yaml

from Crypto.Cipher import AES

with open('client.yaml', "r") as config:
    data = yaml.load(config)

class Client:
    
    def __init__(self, sender, key_file):
        address = 'localhost'
        port = data['port']

        self.sender = sender
        
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = messenger_pb2_grpc.MessengerServerStub(channel)

        user = messenger_pb2.User()
        user.user = self.sender
        response = self.conn.ValidateUser(user)

        if response.message != "":
            print(response.message)
            sys.exit()

        registered_users = response.user_list.split(",")
        registered_users.remove(self.sender)
        print('[Spartan] User list: ' + ",".join(registered_users))
        
        temp_user = messenger_pb2.User()
        temp_user.user = self.sender
        requested_user_list = self.conn.ReturnUsers(temp_user)

        if len(requested_user_list.user) > 0:
            requested_users = requested_user_list.user.split(",") 
            confirmation = input("[Spartan] " + str(requested_users[0]) + " is requesting to chat with you. Enter 'yes' to accept or different user: ")
            if confirmation == 'yes':
                receiver = str(requested_users[len(requested_users) - 1])
            else:
                receiver = confirmation
        else:
            receiver = input('[Spartan] Enter a user whom you want to chat with: ')

        user = messenger_pb2.User()
        user.user = receiver
        response = self.conn.ValidateUser(user)

        if response.message != "":
            print(response.message)
            sys.exit()
        
        self.receiver = receiver

        chat_key = messenger_pb2.Key()
        chat_key.key = self.sender + "<>" + self.receiver

        register_resp = self.conn.RegisterKey(chat_key)

        print('[Spartan] You are now ready to chat with ' + self.receiver)
        
        file = open(key_file, "rb")
        self.cipher_key = file.read()

        threading.Thread(target=self.CheckForMessages, daemon=True, args={}).start()

    def CheckForMessages(self):

        # Creating Key
        key = messenger_pb2.Key()
        key.key = self.sender + "<>" + self.receiver

        for text in self.conn.MessageStream(key):
            cipher = AES.new(self.cipher_key, AES.MODE_EAX, text.cipher)
            data = cipher.decrypt_and_verify(text.cipher_text, text.tag)
            print("[{}] > {}".format(text.sender, data.decode('utf-8')))
    
    def SendMessage(self):
            response = self.conn.SendMessage(self.GetUserInput())
            for resp in response:
                if len(resp.message) != 0:
                    print(resp.message)


    def GetUserInput(self):
        print("Enter a message or (q) to quit: ")
        while True:
            time.sleep(0.2)
            message = input()
            if message == "q":
                sys.exit()
            else:
                if message is not '':
                    n = messenger_pb2.Text()
                    n.sender = self.sender
                    n.receiver = self.receiver
                    data = message.encode('utf-8')
                    encryption_suite = AES.new(self.cipher_key, AES.MODE_EAX)
                    cipher_text, tag = encryption_suite.encrypt_and_digest(data)
                    n.cipher_text = cipher_text
                    n.tag = tag
                    n.cipher = encryption_suite.nonce
                    yield n


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please run the client with a username")
        sys.exit()

    sender = sys.argv[1]

    key = data['key']
    print('[Spartan] Connected to Spartan Server at port {}.'.format(data['port']))
    
    c = Client(sender, key)
    c.SendMessage()