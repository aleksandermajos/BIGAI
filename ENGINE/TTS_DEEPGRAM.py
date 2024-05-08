import requests
from KEY_DEEPGRAM import provide_key

# Define the API endpoint
url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"

# Set your Deepgram API key
api_key = provide_key()
api_key = api_key.strip()

# Define the headers
headers = {
    "Authorization": f"Token {api_key}",
    "Content-Type": "application/json"
}

# Define the payload
payload = {
    "text": "読者である子どものみなさん、この本を一人の大人にささげたことを許してほしい。それには大切な理由がある。まず、この人は世界で一番の私の親友なのだ。次に、この大人は何でもわかる人なのだ、子どもについての本でさえ。そしてもう一つの理由。このは今フランスに住んでいて、おなかをすかせて、寒い思いをしている。彼には励ましが必要だ。こういった理由でも納得してもらえないならば、この本を子どもだったころのその大人にささげることにしよう。どんな大人もかつては子どもだったのだから（とは言っても、それを覚えている人はほとんどいないのだが）。そういうわけで、この献辞は次のように修正する。"
}

# Make the POST request
response = requests.post(url, headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Save the response content to a file
    with open("your_output_file.mp3", "wb") as f:
        f.write(response.content)
    print("File saved successfully.")
else:
    print(f"Error: {response.status_code} - {response.text}")