import requests
from translate import translate_instruction

OSRM = "https://router.project-osrm.org"
UA = {"User-Agent": "VietnamPlace/1.0 (contact: bsssdd24@gmail.com)"}

def get_route(lon1, lat1, lon2, lat2):
    r = requests.get(f"{OSRM}/route/v1/driving/{lon1},{lat1};{lon2},{lat2}",
                    params={
                        "overview": "full", 
                        "geometries": "geojson",
                        "steps": "true",           
                        "annotations": "true"      
                    }, headers=UA, timeout=30)
    r.raise_for_status()
    data = r.json()
    route = data["routes"][0]
    coords = [[lat, lon] for lon, lat in route["geometry"]["coordinates"]]
    
    # xử lý chỉ đường
    steps = []
    for leg in route["legs"]:
        for step in leg["steps"]:
            instruction = step.get("maneuver", {})
            steps.append({
                "instruction": translate_instruction(instruction.get("type"), instruction.get("modifier")),
                "distance": round(step["distance"], 0),
                "duration": round(step["duration"] / 60, 1),
                "name": step.get("name", "đường không tên")
            })
    
    return {
        "coordinates": coords,
        "distance_km": round(route["distance"] / 1000, 1),
        "duration_min": round(route["duration"] / 60, 0),
        "steps": steps  
    }