from flask import Flask, request, jsonify, send_file
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image

app = Flask(__name__, static_folder='static')

# Define radar chart labels
TRAITS = ["Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism", "Openness"]


def create_radar_chart(scores, filename):
    angles = np.linspace(0, 2 * np.pi, len(TRAITS), endpoint=False).tolist()
    scores += scores[:1]  # Close the chart
    angles += angles[:1]

    # Set figure size to match desired dimensions (15cm x 10cm)
    fig, ax = plt.subplots(figsize=(5.9, 3.9), subplot_kw={'projection': 'polar'})  # 1 inch = 2.54 cm
    ax.fill(angles, scores, color='blue', alpha=0.4)
    ax.plot(angles, scores, color='blue', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(TRAITS, fontsize=10)  # Adjust font size for better fit

    # Add padding around the chart to prevent cropping
    fig.subplots_adjust(top=0.85, bottom=0.15, left=0.15, right=0.85)

    static_dir = os.path.join(os.getcwd(), "static")
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Save as PNG first, then convert to JPEG to ensure proper encoding
    png_path = os.path.join(static_dir, filename.replace('.jpeg', '.png'))
    jpeg_path = os.path.join(static_dir, filename)
    plt.savefig(png_path, format='png', bbox_inches='tight', pad_inches=0.5)  # Add padding to ensure nothing is cropped
    plt.close(fig)

    # Convert PNG to JPEG using PIL
    with Image.open(png_path) as img:
        rgb_img = img.convert('RGB')  # Ensure proper JPEG encoding
        rgb_img.save(jpeg_path, format='JPEG', quality=95)

    os.remove(png_path)  # Remove intermediate PNG file
    return jpeg_path


@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    try:
        data = request.json
        scores = [
            data.get("Extraversion", 0),
            data.get("Agreeableness", 0),
            data.get("Conscientiousness", 0),
            data.get("Neuroticism", 0),
            data.get("Openness", 0)
        ]

        if not all(isinstance(score, (int, float)) for score in scores):
            return jsonify({'error': 'All values must be numeric'}), 400

        # Generate unique filename to avoid cache issues
        filename = f"radar_chart_{np.random.randint(100000)}.jpeg"
        image_path = create_radar_chart(scores, filename)

        # Return image directly with correct MIME type
        return send_file(image_path, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def home():
    return jsonify({"message": "Radar Chart API is running. Use POST /generate_chart to generate charts."})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# requirements.txt
# Flask==2.0.3
# matplotlib==3.5.1
# numpy==1.21.2
# Pillow==9.0.1
