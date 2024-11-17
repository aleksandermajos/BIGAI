from KEY_OPENAI import provide_key
api_key = provide_key()
from playsound import playsound

import json
import asyncio
import websockets

# Define the WebSocket URL and API key
url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
api_key = api_key


# Function to handle WebSocket connection and messages
async def connect():
    # Set the headers for authentication and beta access
    headers = {
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "realtime=v1"
    }

    # Connect to the WebSocket
    async with websockets.connect(url, extra_headers=headers) as ws:
        print("Connected to server.")
        event = {
            "type": "session.update",
            "session": {
                "modalities": ["audio", "text"],
                "instructions": "Your knowledge cutoff is 2023-10. You are a helpful assistant called Aris",
                "voice": "shimmer",
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "input_audio_transcription": {
                    # "enabled": True,
                    "model": "whisper-1"
                },
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.1,
                    "prefix_padding_ms": 10,
                    "silence_duration_ms": 999
                },
            }
        }
        await ws.send(json.dumps(event))

        async for response in ws:
            res_1 = json.loads(response)
            # print(res_1)
            if res_1["type"] == "session.updated":
                text_message = {
                    'event_id': res_1['event_id'],
                    "type": "conversation.item.create",
                    "item": {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": "what is 5+5"}]
                    }
                }
                await ws.send(json.dumps(text_message))

                async for response in ws:
                    res = json.loads(response)

                    # print(res)
                    if res['type'] == 'conversation.item.created':

                        message = {
                            'event_id': res['event_id'],
                            "type": "response.create",
                            "response": {
                                "modalities": ["audio", "text"],
                                "voice": "alloy",
                                "instructions": "make joke about this",
                                "output_audio_format": "pcm16"

                            }

                        }
                        await ws.send(json.dumps(message))
                        i = 1
                        async for response in ws:
                            result = json.loads(response)

                            if result['type'] == 'response.text.delta':
                                print(result['delta'])
                            if result['type'] == "response.audio.delta":
                                import base64
                                sample_rate = 19000  # Replace with your actual sample rate
                                output_audio = base64.b64decode(result["delta"])  # Replace with your actual audio data
                                import wave
                                # Create a new wave file
                                with wave.open(f'output{i}.wav', 'wb') as wf:
                                    # Set the parameters
                                    wf.setnchannels(1)  # Mono audio
                                    wf.setsampwidth(2)  # 16-bit audio
                                    wf.setframerate(sample_rate)

                                    # Write the audio data to the file
                                    wf.writeframes(output_audio)
                                playsound(f'output{i}.wav')
                                del result["delta"]
                                i += 1
                            # else:
                            #         print(result)

                            if result['type'] == 'response.done':
                                # break
                                return 1
                    print(json.loads(response))

            # else:
            #     print("//////////////////\n")


# Run the async WebSocket connection
asyncio.run(connect())
