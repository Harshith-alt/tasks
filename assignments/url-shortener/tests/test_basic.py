import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_valid_url(client):
    response = client.post('/api/shorten', json={"url": "https://example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "short_code" in data
    assert "short_url" in data

def test_shorten_invalid_url(client):
    response = client.post('/api/shorten', json={"url": "not_a_url"})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == "Invalid or missing URL"

def test_redirect_existing_code(client):
    # First create a shortened URL
    create = client.post('/api/shorten', json={"url": "https://example.com"})
    short_code = create.get_json()["short_code"]

    # Then try accessing it
    response = client.get(f'/{short_code}', follow_redirects=False)
    assert response.status_code == 302  # Should redirect
    assert response.headers['Location'] == "https://example.com"

def test_redirect_invalid_code(client):
    response = client.get('/nonexistent123')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "Short URL not found"

def test_stats_endpoint(client):
    # Create shortened URL
    create = client.post('/api/shorten', json={"url": "https://example.com"})
    short_code = create.get_json()["short_code"]

    # Get stats
    stats = client.get(f'/api/stats/{short_code}')
    assert stats.status_code == 200
    data = stats.get_json()
    assert data['url'] == "https://example.com"
    assert "clicks" in data
    assert "created_at" in data
