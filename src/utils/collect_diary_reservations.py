import requests
import json
import pandas as pd
from datetime import datetime


def collect_data(API_KEY: str):
    today_date = datetime.now()
    today_date_formatted = today_date.strftime("%d/%m/%Y")
    headers = {'x-api-key': API_KEY}
    created = {'from': today_date_formatted, 'to': today_date_formatted}
    all_reservations = []
    limit = 64
    offset = 0
    has_more_reservations = True

    while has_more_reservations:
        pager = {'limit': limit, 'offset': offset}
        data = {'created': created, 'pager': pager}
        data = {'filters': json.dumps(data)}
        
        response = requests.post(
            'https://kapi.wubook.net/kp/reservations/fetch_reservations',
            headers=headers, data=data)
        
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
