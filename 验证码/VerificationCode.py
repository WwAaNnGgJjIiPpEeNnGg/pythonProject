import os
import random
import uuid
from flask import Flask, render_template, request, jsonify, session, send_file
from PIL import Image, ImageDraw

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Constants for the captcha
CAPTCHA_WIDTH = 300
CAPTCHA_HEIGHT = 150
SLIDER_WIDTH = 60
SLIDER_HEIGHT = 50


def generate_captcha():
    # Create a blank image with a random background color
    captcha_image = Image.new('RGB', (CAPTCHA_WIDTH, CAPTCHA_HEIGHT), color=(255, 255, 255))

    # Generate a random slider position (x-coordinate of the left corner of the slider)
    slider_pos = random.randint(SLIDER_WIDTH, CAPTCHA_WIDTH - SLIDER_WIDTH)

    # Draw the slider on the captcha image
    draw = ImageDraw.Draw(captcha_image)
    draw.rectangle([slider_pos, CAPTCHA_HEIGHT // 2 - SLIDER_HEIGHT // 2,
                    slider_pos + SLIDER_WIDTH, CAPTCHA_HEIGHT // 2 + SLIDER_HEIGHT // 2], fill='blue')

    # Generate a unique filename for the captcha image
    captcha_image_filename = f'captcha_{uuid.uuid4()}.png'
    captcha_image_path = os.path.join('static', captcha_image_filename)

    # Save the captcha image to the generated filename
    captcha_image.save(captcha_image_path)

    # Delete the old captcha image file if it exists
    old_captcha_image_path = session.get('captcha_image_path')
    if old_captcha_image_path and os.path.exists(old_captcha_image_path):
        os.remove(old_captcha_image_path)

    session['captcha_image_path'] = captcha_image_path

    return captcha_image_filename, slider_pos


@app.route('/')
def index():
    # Generate a new captcha and store the necessary data in the session
    captcha_image_filename, slider_pos = generate_captcha()
    session['slider_pos'] = slider_pos
    session['captcha_passed'] = False
    return render_template('index.html', captcha_image=captcha_image_filename)


@app.route('/captcha_image')
def captcha_image():
    captcha_image_path = session.get('captcha_image_path')
    if captcha_image_path and os.path.exists(captcha_image_path):
        return send_file(captcha_image_path, mimetype='image/png')
    else:
        return 'Captcha image not found', 404


@app.route('/verify', methods=['POST'])
def verify():
    # Get the x-coordinate of the user's submitted slider position
    user_slider_pos = int(request.form['slider_pos'])

    # Get the expected slider position from the session
    expected_slider_pos = session.get('slider_pos')

    # Verify if the user's slider position is close to the expected position (allowing a small tolerance)
    if abs(user_slider_pos - expected_slider_pos) <= 5:
        session['captcha_passed'] = True
        return jsonify({'message': 'Success! Captcha passed.'})
    else:
        return jsonify({'message': 'Error! Captcha failed.'})


if __name__ == '__main__':
    app.run(debug=True)
