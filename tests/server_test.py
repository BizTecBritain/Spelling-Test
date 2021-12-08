import time
from communications.data_channel import DataChannel

time.sleep(5)
channel = DataChannel("127.0.0.1", 5000)

session_id = channel.get_text("login/username/password")
headers = None

for i in range(10):
    resp, headers = channel.download_file("get_audio/easy/"+session_id, folder='tests/test_storage/')
    print(resp)
    session_id = headers['session_id']
    resp, headers = channel.get_text_headers("submit_answer/" + session_id + "/" + resp)
    print(resp)
    session_id = headers['session_id']

print(headers['time'])
print(headers['score'])
