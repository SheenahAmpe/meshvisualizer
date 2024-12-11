import requests
import os

# Path to the test graph data file
graph_file_path = 'path-to/graph_data.txt'  # Replace with the path to your graph data file

# Ensure the file exists
if not os.path.exists(graph_file_path):
    print(f"Error: File not found at {graph_file_path}")
    exit(1)

# API endpoint for uploading the graph file
api_url = 'http://172.17.0.2:5000/visualize'

def test_visualize_api(graph_file, download_folder):
    # Open the file in binary mode and post it to the API
    with open(graph_file, 'rb') as f:
        files = {'file': f}
        response = requests.post(api_url, files=files)
    
    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        image_url = result.get('image_path')
        if image_url:
            fetch_and_display_image(f"http://localhost:5000{image_url}", download_folder)
        else:
            print("Image path not found in response.")
    else:
        print("Error:", response.status_code, response.text)

def fetch_and_display_image(image_url, download_folder):
    # Send a request to download the image
    response = requests.get(image_url, stream=True)
    response.raise_for_status()  # Raise exception for HTTP errors

    # Create the download folder if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)

    # Define the image path
    image_path = os.path.join(download_folder, 'downloaded_graph_visualization.png')

    # Save the image locally
    with open(image_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f'Image downloaded to: {image_path}')

    # # Display the image using matplotlib
    # import matplotlib.pyplot as plt
    # import matplotlib.image as mpimg

    # img = mpimg.imread(image_path)
    # plt.imshow(img)
    # plt.axis('off')
    # plt.show()

# Run the test, specify your desired download folder
download_folder = '/home/jalvin/Libraries/graph'  # Change this to your desired directory
test_visualize_api(graph_file_path, download_folder)
