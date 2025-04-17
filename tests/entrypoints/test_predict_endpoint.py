import io
from counter.entrypoints import webapp


def test_predict_endpoint_returns_predictions():
    app = webapp.create_app()
    client = app.test_client()

    # Load a sample image as binary (replace this with your real image file)
    with open('tests/assets/sample.jpg', 'rb') as f:
        image_data = f.read()

    data = {
        'threshold': '0.5',
        'file': (io.BytesIO(image_data), 'sample.jpg')
    }

    response = client.post('/predict', data=data, content_type='multipart/form-data')

    # Print the status code and response JSON for debugging
    print(f"Response Status Code: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")  # This will print the JSON response from the endpoint

    # Make sure the response code is 200 (OK)
    assert response.status_code == 200

    # Optionally, assert some fields in the response JSON
    response_json = response.get_json()
    assert 'predictions' in response_json
    assert isinstance(response_json['predictions'], list)
