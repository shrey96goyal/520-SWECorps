import requests
import pytest
import json

def test_validate_max_elevation_request():
    print("Validating max elevation request received from front-end")
    request_api = "http://127.0.0.1:5000/path?elevation=2&distance=80&src_lat=42.3772684&src_lang=-72.5194994&dest_lat=42.3495879&dest_lang=-72.5283459"
    x = requests.get(request_api)
    responseJSON = json.loads(x.text)
    print(responseJSON)
    assert x.status_code == 200
    assert responseJSON["distance"] >= 3449.476 
    assert responseJSON["distance"] <= 3449.476*1.8
    assert responseJSON["elevation"] >= 1.161

def test_validate_min_elevation_request():
    print("Validating min elevation request received from front-end")
    request_api = "http://127.0.0.1:5000/path?elevation=1&distance=80&src_lat=42.3772684&src_lang=-72.5194994&dest_lat=42.3495879&dest_lang=-72.5283459"
    x = requests.get(request_api)
    responseJSON = json.loads(x.text)
    assert x.status_code == 200
    assert responseJSON["distance"] >= 3449.476 
    assert responseJSON["distance"] <= 3449.476*1.8
    assert responseJSON["elevation"] <= 1.161

def test_invalid_source_request():
    print("Validating min elevation request received from front-end")
    request_api = "http://127.0.0.1:5000/path?elevation=1&distance=80&src_lat=&src_lang=&dest_lat=42.3495879&dest_lang=-72.5283459"
    x = requests.get(request_api)
    responseJSON = json.loads(x.text)
    assert x.status_code == 400
    assert "message" in responseJSON

def test_invalid_target_request():
    print("Validating min elevation request received from front-end")
    request_api = "http://127.0.0.1:5000/path?elevation=1&distance=80&src_lat=42.3772684&src_lang=-72.5194994&dest_lat=&dest_lang="
    x = requests.get(request_api)
    responseJSON = json.loads(x.text)
    assert x.status_code == 400
    assert "message" in responseJSON

def test_invalid_elevation_request():
    print("Validating min elevation request received from front-end")
    request_api = "http://127.0.0.1:5000/path?elevation=3&distance=80&src_lat=42.3772684&src_lang=-72.5194994&dest_lat=42.3495879&dest_lang=-72.5283459"
    x = requests.get(request_api)
    responseJSON = json.loads(x.text)
    assert x.status_code == 400
    assert "message" in responseJSON

def test_invalid_distance_percentage_request():
    print("Validating min elevation request received from front-end")
    request_api = "http://127.0.0.1:5000/path?elevation=1&distance=-8&src_lat=42.3772684&src_lang=-72.5194994&dest_lat=42.3495879&dest_lang=-72.5283459"
    x = requests.get(request_api)
    responseJSON = json.loads(x.text)
    assert x.status_code == 400
    assert "message" in responseJSON