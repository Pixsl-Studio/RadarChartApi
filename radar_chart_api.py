from flask import Flask, request, jsonify, send_file
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)

# Define radar chart labels
TRAITS = ["Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism", "Openness"]

def create_radar_chart(scores):
    angles = np.linspace(0, 2 * np.pi, len(TRAITS), endpoint=False).tolist()
    scores += scores[:1]  # Close the chart
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
    ax.fill(angles, scores, color='blue', alpha=0.4)
    ax.plot(angles, scores, color='blue', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(TRAITS)

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plt.close(fig)
    return img_bytes

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

        img_bytes = create_radar_chart(scores)
        return send_file(img_bytes, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
