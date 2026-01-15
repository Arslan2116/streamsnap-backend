import requests

api_url = "http://127.0.0.1:5000/get-video"
test_link = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

print("⏳ Connecting to Render Server...")

try:
    # Server ko request bhejna
    response = requests.post(api_url, json={"url": test_link})
    
    # Jawab dekhna
    data = response.json()
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! Server ne jawab diya:")
        print(f"Title: {data.get('title')}")
        print(f"Download URL: {data.get('download_url')}")
    else:
        print("\n❌ ERROR aaya:")
        print(data)

except Exception as e:
    print(f"\n❌ Connection Failed: {e}")