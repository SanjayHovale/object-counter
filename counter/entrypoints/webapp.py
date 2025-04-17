# from io import BytesIO

# from flask import Flask, request, jsonify

# from counter import config

# from PIL import Image

# from counter.adapters.sqlalchemy.object_count_repo import ObjectCountRepo
# from counter.adapters.sqlalchemy.db import SessionLocal  # Use the session from db.py
# from counter.adapters.sqlalchemy.models import ObjectCount
# def create_app():
    
#     app = Flask(__name__)
    
#     count_action = config.get_count_action()
    
#     @app.route('/object-count', methods=['POST'])
#     def object_detection():
        
#         threshold = float(request.form.get('threshold', 0.5))
#         uploaded_file = request.files['file']
#         model_name = request.form.get('model_name', "rfcn")
#         image = BytesIO()
#         uploaded_file.save(image)
#         count_response = count_action.execute(image, threshold)

        
#         return jsonify(count_response)

#     @app.route('/predict', methods=['POST'])
#     def predict_objects():
#         threshold = float(request.form.get('threshold', 0.5))  # Get threshold from the request
#         uploaded_file = request.files.get('file')

#         if not uploaded_file:
#             return jsonify({'error': 'No file uploaded'}), 400

#         image = BytesIO()
#         uploaded_file.save(image)

#         # Get predictions from count_action.execute
#         count_response = count_action.execute(image, threshold)

#         # Debugging: Check the response structure
#         print(f"CountResponse: {count_response}")

#         # Access predictions from current_objects
#         predictions = count_response.current_objects  # Adjust based on the structure of CountResponse

#         # Filter and format predictions
#         filtered = [p for p in predictions if p.count >= threshold]  # Use `count` instead of `confidence`

#         # Debugging: Check filtered predictions
#         print(f"Filtered Predictions: {filtered}")

#         result = []
#         for p in filtered:
#             result.append({
#                 'label': p.object_class,  # Assuming 'object_class' is the label
#                 'confidence': round(p.count, 2)  # Assuming 'count' represents the confidence
#             })

#         # Debugging: Check the final response before returning
#         print(f"Response: {result}")

#         return jsonify({
#             'threshold': threshold,
#             'predictions': result,
#             'total': len(result)
#         })


        
    
#     return app



# if __name__ == '__main__':
#     app = create_app()
#     app.run('0.0.0.0', debug=True)

from io import BytesIO
from flask import Flask, request, jsonify
from counter import config
from counter.adapters.sqlalchemy.object_count_repo import ObjectCountRepo
from PIL import Image


def create_app():
    app = Flask(__name__)

    count_action = config.get_count_action()
    repo = ObjectCountRepo()  # Initialize the PostgreSQL adapter

    @app.route('/object-count', methods=['POST'])
    def object_detection():
        threshold = float(request.form.get('threshold', 0.5))
        uploaded_file = request.files['file']
        model_name = request.form.get('model_name', "rfcn")

        image = BytesIO()
        uploaded_file.save(image)

        # Run the object detection
        count_response = count_action.execute(image, threshold)

        # Save detected objects to DB
        for obj in count_response.current_objects:
            if obj.count >= threshold:
                repo.save_object_count(object_type=obj.object_class, count=obj.count)

        return jsonify({
            "status": "saved",
            "total_saved": len(count_response.current_objects),
            "threshold": threshold
        })

    @app.route('/predict', methods=['POST'])
    def predict_objects():
        threshold = float(request.form.get('threshold', 0.5))
        uploaded_file = request.files.get('file')

        if not uploaded_file:
            return jsonify({'error': 'No file uploaded'}), 400

        image = BytesIO()
        uploaded_file.save(image)

        # Get predictions from count_action
        count_response = count_action.execute(image, threshold)

        predictions = count_response.current_objects  # List of predicted objects

        filtered = [p for p in predictions if p.count >= threshold]

        result = []
        for p in filtered:
            result.append({
                'label': p.object_class,
                'confidence': round(p.count, 2)
            })

        return jsonify({
            'threshold': threshold,
            'predictions': result,
            'total': len(result)
        })

    @app.route('/object-counts', methods=['GET'])
    def get_all_object_counts():
        # Fetch all records from the database
        all_counts = repo.get_all_counts()

        # Format the records into a JSON-serializable list
        results = []
        for entry in all_counts:
            results.append({
                "id": entry.id,
                "object_type": entry.object_type,
                "count": entry.count,
                "timestamp": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S") if entry.timestamp else None
            })

        return jsonify(results)
    

    return app


if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', debug=True)
