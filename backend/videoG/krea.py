import requests
import time

# Insert your AI/ML API key instead of <YOUR_AIMLAPI_KEY>:


# Creating and sending a video generation task to the server
def generate_video(promt, api_key):
    url = "https://api.aimlapi.com/v2/video/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    
    data = {
        "model": "krea/krea-wan-14b/text-to-video",
        "prompt": promt,
        "num_frames": 90
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code >= 400:
        print(f"Error: {response.status_code} - {response.text}")
    else:
        response_data = response.json()
        print(response_data)
        return response_data


# Requesting the result of the task from the server using the generation_id
def get_video(gen_id, api_key):
    url = "https://api.aimlapi.com/v2/video/generations"
    params = {
        "generation_id": gen_id,
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def main(promt, api_key):
    # Generate video
    gen_response = generate_video(promt, api_key)
    gen_id = gen_response.get("id")
    print("Generation ID:  ", gen_id)
    
    # Try to retrieve the video from the server every 10 sec
    if gen_id:
        start_time = time.time()
        
        timeout = 600
        while time.time() - start_time < timeout:
            response_data = get_video(gen_id, api_key)
            
            if response_data is None:
                print("Error: No response from API")
                break
            
            status = response_data.get("status")
            print("Status:", status)
            
            if status == "waiting" or status == "active" or status == "queued" or status == "generating":
                print("Still waiting... Checking again in 10 seconds.")
                time.sleep(10)
            else:
                print("Processing complete:/n", response_data)
                return response_data
        
        print("Timeout reached. Stopping.")
        return None


if __name__ == "__main__":
    api_key = "a********"
    promt = "A menacing evil dragon appears in a distance above the tallest mountain, then rushes toward the camera with its jaws open, revealing massive fangs. We see it's coming."
    main(promt, api_key)