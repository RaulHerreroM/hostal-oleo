import requests
import json
import pandas as pd
from config.config import settings


def collect_data(API_KEY: str,
                 created_date_from: str,
                 created_date_to: str,
                 arrival_date_from: str,
                 arrival_date_to: str):

    headers = {'x-api-key': API_KEY}
    created = {'from': created_date_from, 'to': created_date_to}
    arrival = {'from': arrival_date_from, 'to': arrival_date_to}
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
            
            reservations = response_json.get('data',
                                             {}).get('reservations', [])
            
            if not reservations:
                has_more_reservations = False
            else:
                all_reservations.extend(reservations)
                offset += limit
        else:
            print(f"ERROR: {response.status_code}")
            has_more_reservations = False

    reservations_data = []

    for reservation in all_reservations:
        reservation_id = reservation.get('id')
        status = reservation.get('status')
        origin = reservation.get('origin', {}).get('channel')
        created = reservation.get('created')
        total_price = reservation.get('price', {}).get('total')
        
        n_rooms = len(reservation.get('rooms', []))
        
        if n_rooms > 0:
            dfrom = reservation.get('rooms')[0].get('dfrom')
            dto = reservation.get('rooms')[0].get('dto')
        else:
            dfrom = None
            dto = None
            
        reservations_data.append({
            'id': reservation_id,
            'status': status,
            'origin': origin,
            'created': created,
            'n_rooms': n_rooms,
            'dfrom': dfrom,
            'dto': dto,
            'total_price': total_price
        })

    df = pd.DataFrame(reservations_data)
    return df

