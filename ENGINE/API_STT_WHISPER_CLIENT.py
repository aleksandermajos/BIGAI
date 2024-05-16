import subprocess

def curl_request(url):
    command = ['curl', '-s', '-o', '-', url]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

response = curl_request(r'-X POST "http://127.0.0.1:8000/transcribe/" -F "file=@example.wav"')
print(response)