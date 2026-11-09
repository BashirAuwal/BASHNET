import uuid
import json
from datetime import datetime


class BashNetCore:

    def __init__(self, device_name):

        self.device_name = device_name

        self.device_id = str(uuid.uuid4())[:8]

        self.status = "OFFLINE"


    def create_message(self, receiver_id, message_text):

        message = {

            "message_id": str(uuid.uuid4()),

            "sender_id": self.device_id,

            "receiver_id": receiver_id,

            "message": message_text,

            "timestamp": datetime.now().isoformat(),

            "status": "PENDING"

        }

        return message


    def encode_message(self, message):

        return json.dumps(message)


    def show_device(self):

        print("\n====== BASHNET ======")

        print("Device:", self.device_name)

        print("Device ID:", self.device_id)

        print("Status:", self.status)

        print("=====================")


# Create BASHNET device

my_device = BashNetCore("BASHIR")

my_device.show_device()


# Create a message

new_message = my_device.create_message(

    "BASHCO002",

    "Assalamu Alaikum. Wannan sakon BASHNET ne."

)


# Convert message to JSON

encoded_message = my_device.encode_message(new_message)


print("\nMESSAGE CREATED")

print(encoded_message)