from concurrent import futures

import grpc
import time
import messenger_pb2
import messenger_pb2_grpc
import Lru_Cache
import threading

import yaml

with open('config.yaml', "r") as config:
    data = yaml.load(config)

class ChatServer(messenger_pb2_grpc.MessengerServerServicer):

    CACHE_CAPACITY = data['max_num_messages_per_user']
    LRU_TIME_LIMIT = 24 * 60 * 60
    RATE_TIME_LIMIT = 30
    RATE_MESSAGE_LIMIT = data['max_call_per_30_seconds_per_user']

    def __init__(self):
        self.messages = {}
        self.indexes = {}
        self.read_index = {}
        self.sender_timer = {}

    def ReturnUsers(self, request_iterator, context):
        user = request_iterator.user
        requested_users = list()

        for key in self.messages.keys():
            if user in key:
                name1 = key.split('<>')[0]
                name2 = key.split('<>')[1]

                if name1 == user:
                    requested_users.append(name2)
                else:
                    requested_users.append(name1)
        
        user_list = messenger_pb2.User()
        user_list.user = ','.join(requested_users)

        return user_list

    def RegisterKey(self, request_iterator, context):
        key = request_iterator.key
        
        sender = key.split('<>')[0]
        receiver = key.split('<>')[1]
        
        participants = list()
        participants.append(key.split('<>')[0])
        participants.append(key.split('<>')[1])
        participants = sorted(participants)

        key = participants[0] + '<>' + participants[1]
        if key not in self.messages.keys():
            self.messages[key] = Lru_Cache.Lru_Cache(self.CACHE_CAPACITY)

        if participants[0] not in self.read_index.keys():
            self.read_index[participants[0]] = 0

        if participants[1] not in self.read_index.keys():
            self.read_index[participants[1]] = 0

        resp = messenger_pb2.Empty()
        return resp

    def ValidateUser(self, request_iterator, context):
        registered_user = data['users']
        user = request_iterator.user
        confirmation = messenger_pb2.SendConfirmation() 
        confirmation.user_list = ','.join(registered_user)
        if user not in registered_user:
            confirmation.message = "[Spartan] Not a registered user"
        else:
            confirmation.message = ""
        
        return confirmation

    def MessageStream(self, request_iterator, context):
        key = request_iterator.key

        sender = key.split('<>')[0]
        receiver = key.split('<>')[1]
        
        participants = list()
        participants.append(key.split('<>')[0])
        participants.append(key.split('<>')[1])
        participants = sorted(participants)

        key = participants[0] + '<>' + participants[1]

        while True:
            if key in self.messages:
                count = self.messages[key].delete_old_message(self.LRU_TIME_LIMIT)
                if count > 0:
                    self.read_index[sender] = max(0, self.read_index[sender] - count)
                    self.read_index[receiver] = max(0, self.read_index[receiver] - count)
                
                msgs = self.messages[key].print_cache()
                while self.read_index[sender] < len(msgs):

                    self.read_index[sender] = self.read_index[sender] + 1
                    yield msgs[self.read_index[sender]-1]
  

    def SendMessage(self, request, context):
        
        for message in request:
            if message.sender not in self.sender_timer:
                self.sender_timer[message.sender] = list()
                self.sender_timer[message.sender].append(time.time())

            else:
                if int(time.time() - self.sender_timer[message.sender][0]) <= self.RATE_TIME_LIMIT:
                    if len(self.sender_timer[message.sender]) == self.RATE_MESSAGE_LIMIT:
                        confirmation = messenger_pb2.SendConfirmation()
                        confirmation.message = "[Spartan] Rate limit exceeded"
                        yield confirmation
                        continue
                    else:
                        self.sender_timer[message.sender].append(time.time())
                else:
                    if len(self.sender_timer[message.sender]) < self.RATE_MESSAGE_LIMIT:
                        self.sender_timer[message.sender].append(time.time())
                    else:
                        i = 0
                        while i < len(self.sender_timer[message.sender]) and int(time.time() - self.sender_timer[message.sender][i]) > self.RATE_TIME_LIMIT:
                            i = i + 1
                        
                        self.sender_timer[message.sender] = self.sender_timer[message.sender][i:]
                        self.sender_timer[message.sender].append(time.time())

            # Creating key
            participants = list()
            participants.append(message.sender)
            participants.append(message.receiver)
            participants = sorted(participants)
            key = participants[0] + "<>" + participants[1]  

            if message.sender not in self.read_index:
                self.read_index[message.sender] = 0

            if message.receiver not in self.read_index:
                self.read_index[message.receiver] = 0       
            
            if key not in self.messages:
                self.messages[key] = Lru_Cache.Lru_Cache(self.CACHE_CAPACITY)

            if key not in self.indexes:
                self.indexes[key] = 0

            if self.messages[key].cache_len() == self.CACHE_CAPACITY:
                if self.read_index[message.receiver] > 0:
                    self.read_index[message.receiver] = self.read_index[message.receiver] - 1
                if self.read_index[message.sender] > 0:
                    self.read_index[message.sender] = self.read_index[message.sender] - 1

            self.messages[key].set(str(time.time()), message)

            print(message)
            
            confirmation = messenger_pb2.SendConfirmation()
            confirmation.message = ""

            yield confirmation
    

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor())
    messenger_pb2_grpc.add_MessengerServerServicer_to_server(ChatServer(), server)
    address = 'localhost'
    port = 3000
    server.add_insecure_port(address + ':' + str(port))

    server.start()
    print("Spartan server started on port {}.".format(data['port']))

    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)