from page_analyzer.app import app


URL = 'http://127.0.0.1:5000'
app.testing = True

def test_main_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert "<title>Анализатор страниц</title>" in response.text
    
    