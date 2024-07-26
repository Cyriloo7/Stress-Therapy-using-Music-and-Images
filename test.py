import pytest
from flask import Flask
from app import app, data  # Import the Flask app and data from your main application file

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test the index route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Index Page Content" in response.data  # Replace with actual content from your index.html

def test_predict(client, mocker):
    """Test the predict route"""
    
    # Mocking random song selection
    random_song_index = 10
    mocker.patch('random.randint', return_value=random_song_index)
    
    # Mocking SongRecommentation.convert_input_feature
    mocker.patch('app.SongRecommentation.convert_input_feature', return_value='mock_input_feature')

    # Mocking threading.Thread
    mock_thread = mocker.patch('threading.Thread')
    
    # Making POST request to /predict
    response = client.post('/predict', data={'text': 'phobia text'})
    
    assert response.status_code == 200
    assert b"Expected Response Content" in response.data  # Replace with expected response content
    
    # Verify if threads are started correctly
    assert mock_thread.call_count == 2
    mock_thread.assert_any_call(target=app.thread_one, args=(...))  # Complete with appropriate args
    mock_thread.assert_any_call(target=app.thread_two, args=(...))  # Complete with appropriate args
