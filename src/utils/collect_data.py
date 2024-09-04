import requests
import json
import pandas as pd

API-KEY="wb_06064db8-fce1-11ea-90d0-001a4a4ef9b1"


headers = {'x-api-key': API-KEY}
created = {'from': '10/10/2023', 'to': '10/12/2023'}
arrival = {'from': '08/11/2023', 'to': '10/12/2023'}
all_reservations = []
limit = 64
offset = 0
has_more_reservations = True

while has_more_reservations:
    pager = {'limit': limit, 'offset': offset}
    data = {'created': created, 'arrival': arrival, 'pager': pager}
    data = {'filters': json.dumps(data)}

    response = requests.post('https://kapi.wubook.net/kp/reservations/fetch_reservations', headers=headers, data=data)
    
    if response.status_code == 200:
        response_json = response.json()
        reservations = response_json.get('data', {}).get('reservations', [])
        if not reservations:
            has_more_reservations = False
        else:
            all_reservations.extend(reservations)
            offset += limit
    else:
        print(f"Error en la solicitud: {response.status_code}")
        has_more_reservations = False

reservations_data = []

for reservation in all_reservations:
    reservation_id = reservation.get('id')
    status = reservation.get('status')
    origin = reservation.get('origin', {}).get('channel')
    created = reservation.get('created')
    
    num_rooms = len(reservation.get('rooms', []))
    
    for room in reservation.get('rooms', []):
        dfrom = room.get('dfrom')
        dto = room.get('dto')
        occupancy_data = room.get('occupancy', {})
        
        total_occupancy = (occupancy_data.get('adults', 0) +
                           occupancy_data.get('teens', 0) +
                           occupancy_data.get('children', 0) +
                           occupancy_data.get('babies', 0))
        
        total_price = reservation.get('price', {}).get('total')

        reservations_data.append({
            'id': reservation_id,
            'status': status,
            'origin': origin,
            'created': created,
            'dfrom': dfrom,
            'dto': dto,
            'occupancy': total_occupancy,
            'total_price': total_price,
            'num_rooms': num_rooms 
        })

df = pd.DataFrame(reservations_data)
df.to_csv('../../DATA/reservations.csv', index=False)
