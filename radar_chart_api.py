from flask import Flask, request, jsonify, send_from_directory
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__, static_folder='static')

# Define radar chart labels
TRAITS = ["Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism", "Openness"]


def create_radar_chart(scores, filename):
    angles = np.linspace(0, 2 * np.pi, len(TRAITS), endpoint=False).tolist()
    scores += scores[:1]  # Close the chart
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
    ax.fill(angles, scores, color='blue', alpha=0.4)
    ax.plot(angles, scores, color='blue', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(TRAITS)

    static_dir = os.path.join(os.getcwd(), "static")
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    img_path = os.path.join(static_dir, filename)
    plt.savefig(img_path, format='jpeg')
    plt.close(fig)
    return img_path


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
        create_radar_chart(scores, filename)

        # Construct the public URL
        public_url = request.url_root + f"image/{filename}"

        return jsonify(public_url)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Serve image with correct MIME type
@app.route('/image/<filename>')
def serve_image(filename):
    return send_from_directory('static', filename, mimetype='image/jpeg')


@app.route('/')
def home():
    return jsonify({"message": "Radar Chart API is running. Use POST /generate_chart to generate charts."})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# requirements.txt
# Flask==2.0.3
# matplotlib==3.5.1
# numpy==1.21.2
