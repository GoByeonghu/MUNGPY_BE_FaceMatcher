import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from scipy.spatial.distance import cosine
import glob
import os

from flask import Flask, request, jsonify
app = Flask(__name__)


# Pre-trained model for feature extraction
model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
dog_images_paths = glob.glob('dog_images/*')

def get_dog_face_descriptor(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = model.predict(img_data)
    return features.flatten()


def find_top_n_similar(input_descriptor, dog_descriptors, n=5):
    similarities = [1 - cosine(input_descriptor, desc) for desc in dog_descriptors]
    top_n_indices = np.argsort(similarities)[-n:][::-1]  # Get indices of top n similarities
    return [dog_images_paths[idx] for idx in top_n_indices]


# 외부 요청을 처리하기 위한 함수
def handle_request(input_image_path):
    input_descriptor = get_dog_face_descriptor(input_image_path)
    dog_descriptors = [get_dog_face_descriptor(img_path) for img_path in dog_images_paths]
    top_5_similar_dogs = find_top_n_similar(input_descriptor, dog_descriptors, n=5)
    #print(f'Top 5 similar dog images: {top_5_similar_dogs}')
    return top_5_similar_dogs[0]

@app.route('/find_similar_dogs', methods=['POST'])
def find_similar_dogs():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the uploaded file
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    
    # Process the uploaded image
    input_descriptor = get_dog_face_descriptor(file_path)
    
    # Find the most similar dog images
    #top_5_similar_dogs = find_top_n_similar(input_descriptor, dog_descriptors, n=5)
    top_similar_dogs = handle_request(file_path)
    # Clean up uploaded file
    os.remove(file_path)
    
    response = jsonify({"data": top_similar_dogs})
    response.charset = 'utf-8'
    return response


# 예시로 외부 요청을 처리하는 함수 사용
# requested_image_path = 'pms.png'  # 예시 입력 이미지 경로
# result = handle_request(requested_image_path)
# print(f'Result for requested image: {result}')


if __name__ == '__main__':
    # Ensure the 'uploads' directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    app.run(debug=True, port=5000)
