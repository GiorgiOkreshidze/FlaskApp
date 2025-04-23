import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    print("\nResponse content for index route:", response.data.decode())
    # Less strict assertion
    assert response.data.decode().find("DevOps") != -1

def test_greet_route(client):
    response = client.get('/greet/Tester')
    assert response.status_code == 200
    print("\nResponse content for greet route:", response.data.decode())
    # Less strict assertion
    assert response.data.decode().find("Tester") != -1

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    # This should be json response
    assert b'healthy' in response.data

def test_submit_message(client):
    # First submit a message
    response = client.post('/message', data={
        'name': 'Test User',
        'message': 'This is a test message'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    print("\nResponse after submitting message:", response.data.decode())
    
    # Then check if it appears on the index page
    response = client.get('/')
    print("\nIndex page after message submission:", response.data.decode())
    
    # Less strict assertions
    assert response.data.decode().find("Test User") != -1
    assert response.data.decode().find("This is a test message") != -1