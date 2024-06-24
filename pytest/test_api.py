import requests

def test_fetch_todo():
    """Test case to fetch a specific todo item and validate its structure and content."""
    url = 'https://jsonplaceholder.typicode.com/todos/1'
    response = requests.get(url)
    
    # Check if the request was successful (HTTP status code 200)
    assert response.status_code == 200
    
    data = response.json()  # Parse JSON response
    
    # Validate the structure of the response
    assert 'userId' in data
    assert 'id' in data
    assert 'title' in data
    assert 'completed' in data
    
    # Validate the content of the response
    assert data['userId'] == 1
    assert data['id'] == 1
    assert data['title'] == 'delectus aut autem'
    assert data['completed'] is False

def test_post_request():
    """Test case to create a new post using POST request and validate the response."""
    url = 'https://jsonplaceholder.typicode.com/posts'
    payload = {
        'title': 'foo',
        'body': 'bar',
        'userId': 11
    }
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
    }

    # Send POST request with JSON payload
    response = requests.post(url, json=payload, headers=headers)
    
    # Check if the POST request was successful (HTTP status code 201)
    assert response.status_code == 201
    
    data = response.json()  # Parse JSON response
    
    # Validate the structure of the response
    assert 'id' in data
    assert data['title'] == payload['title']
    assert data['body'] == payload['body']
    assert data['userId'] == payload['userId']

def test_put_request():
    """Test case to update an existing post using PUT request and validate the response."""
    url = 'https://jsonplaceholder.typicode.com/posts/1'
    payload = {
        'id': 1,
        'title': 'foo',
        'body': 'bar',
        'userId': 1
    }
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
    }

    # Send PUT request with JSON payload
    response = requests.put(url, json=payload, headers=headers)
    
    # Check if the PUT request was successful (HTTP status code 200)
    assert response.status_code == 200
    
    data = response.json()  # Parse JSON response
    
    # Validate the structure and content of the response
    assert data['id'] == payload['id']
    assert data['title'] == payload['title']
    assert data['body'] == payload['body']
    assert data['userId'] == payload['userId']

def test_patch_request():
    """Test case to partially update an existing post using PATCH request and validate the response."""
    url = 'https://jsonplaceholder.typicode.com/posts/1'
    payload = {
        'title': 'foo'
    }
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
    }

    # Send PATCH request with JSON payload
    response = requests.patch(url, json=payload, headers=headers)
    
    # Check if the PATCH request was successful (HTTP status code 200)
    assert response.status_code == 200
    
    data = response.json()  # Parse JSON response
    
    # Validate that the title was updated correctly
    assert data['title'] == payload['title']

    # Ensure other fields remain unchanged
    assert 'id' in data
    assert 'body' in data
    assert 'userId' in data

def test_delete_request():
    """Test case to delete an existing post using DELETE request and validate the response."""
    url = 'https://jsonplaceholder.typicode.com/posts/1'

    # Send DELETE request
    response = requests.delete(url)
    
    # Check if the DELETE request was successful (HTTP status code 200)
    assert response.status_code == 200

def test_get_user_posts():
    """Test case to fetch posts for a specific user and validate the response."""
    url = 'https://jsonplaceholder.typicode.com/posts'
    params = {'userId': 1}

    # Send GET request with query parameters
    response = requests.get(url, params=params)
    
    # Check if the GET request was successful (HTTP status code 200)
    assert response.status_code == 200
    
    data = response.json()  # Parse JSON response
    
    # Check if the response is a list
    assert isinstance(data, list)
    
    # Check that all posts belong to the user with userId 1
    for post in data:
        assert post['userId'] == 1
        assert 'id' in post
        assert 'title' in post
        assert 'body' in post

def test_fetch_todo_not_found():
    """Test case to fetch a non-existent todo item and expect a 404 response."""
    url = 'https://jsonplaceholder.typicode.com/todos/9999'  # Non-existent ID
    response = requests.get(url)
    
    # Expecting a 404 Not Found status code
    assert response.status_code == 404

def test_put_request_invalid_id():
    """Test case to update a post with an invalid ID and expect a 404 response."""
    url = 'https://jsonplaceholder.typicode.com/posts/9999'  # Non-existent ID
    payload = {
        'id': 9999,
        'title': 'foo',
        'body': 'bar',
        'userId': 1
    }
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
    }

    # Send PUT request with JSON payload
    response = requests.put(url, json=payload, headers=headers)
    
    # Expecting a 404 Not Found status code
    assert response.status_code == 500


if __name__ == '__main__':
    # If this script is run directly, execute all tests using pytest
    import pytest
    pytest.main()
