import boto3
import base64
import subprocess
import threading
import time
import os

# Configurações
camera_url = os.getenv('RTSP_URL')
kinesis_stream_name = os.getenv('KVS_STREAM_NAME')
aws_region = os.getenv('AWS_REGION')
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Inicializar Kinesis Client
kinesis_client = boto3.client('kinesis',
                              region_name=aws_region,
                              aws_access_key_id=aws_access_key,
                              aws_secret_access_key=aws_secret_key)

print(f"RTSP_URL: {camera_url}")
print(f"KINESIS_STREAM_NAME: {kinesis_stream_name}")
print(f"AWS_REGION: {aws_region}")
print(f"AWS_ACCESS_KEY_ID: {aws_access_key}")
print(f"AWS_SECRET_ACCESS_KEY: {aws_secret_key}")

if not aws_region:
    raise ValueError("AWS_REGION environment variable is not set.")

def send_frame_to_kinesis(frame_data):
    frame_base64 = base64.b64encode(frame_data).decode('utf-8')
    response = kinesis_client.put_record(
        StreamName=kinesis_stream_name,
        Data=frame_base64,
        PartitionKey="partitionkey"
    )
    print("Sent frame to Kinesis:", response)


def capture_frames():
    command = [
        'gst-launch-1.0',
        'rtspsrc', f'location={camera_url}', 'latency=0', '!',
        'decodebin', '!',
        'videoconvert', '!',
        'video/x-raw,framerate=1/1', '!',  # 1 frame per second
        'jpegenc', '!',
        'appsink', 'max-buffers=1', 'drop=true'
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        frame_data = process.stdout.read()
        if frame_data:
            send_frame_to_kinesis(frame_data)
        time.sleep(1)  # Garantir que apenas um frame por segundo seja enviado


if __name__ == "__main__":
    capture_thread = threading.Thread(target=capture_frames)
    capture_thread.start()
    capture_thread.join()
