from flask import Flask, request, jsonify, send_file
import os
import tempfile
from meshvisualizerFinal import GraphVisualizer

app = Flask(__name__)
IMAGE_DIR = '/tmp'
LOCAL_GRAPH_DIR = '/app/graph_files' 
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(LOCAL_GRAPH_DIR, exist_ok=True)

graph_visualizer = GraphVisualizer()

@app.route('/visualize', methods=['POST'])
def visualize():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    # Temporarily save the original uploaded file
    temp_file = tempfile.NamedTemporaryFile(delete=False, dir=LOCAL_GRAPH_DIR, suffix='.txt')
    
    try:
        file.save(temp_file.name)
        
        image_path = graph_visualizer.update_graph(temp_file.name)
        return jsonify({'image_path': '/download_image'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Ensure temporary file cleanup
        temp_file.close()
        os.remove(temp_file.name)

@app.route('/download_image', methods=['GET'])
def download_image():
    image_path = os.path.join(IMAGE_DIR, 'graph_visualization.png')
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png', as_attachment=True, download_name='graph_visualization.png')
    else:
        return jsonify({'error': 'Image not found.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)