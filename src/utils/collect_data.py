import requests
import json
import pandas as pd

API-KEY="wb_06064db8-fce1-11ea-90d0-001a4a4ef9b1"


headers = {'x-api-key': API-KEY}
created = {'from': '10/10/2021', 'to': '10/12/2024'}
arrival = {'from': '08/11/2021', 'to': '10/12/2024'}
all_reservations = []
limit = 64
offset = 0
has_more_reservations = True

while has_more_reservations:
    # Crear el cuerpo de la solicitud con el offset actualizado
    pager = {'limit': limit, 'offset': offset}
    data = {'created': created, 'arrival': arrival, 'pager': pager}
    data = {'filters': json.dumps(data)}
    
    # Hacer la solicitud POST
    response = requests.post('https://kapi.wubook.net/kp/reservations/fetch_reservations', headers=headers, data=data)
    
    # Comprobar si la solicitud fue exitosa
    if response.status_code == 200:
        # Obtener los datos de la respuesta
        response_json = response.json()
        
        # Extraer las reservas de la respuesta JSON
        reservations = response_json.get('data', {}).get('reservations', [])
        
        # Si no hay más reservas, terminamos el bucle
        if not reservations:
            has_more_reservations = False
        else:
            # Añadir las reservas obtenidas a la lista total
            all_reservations.extend(reservations)
            
            # Incrementar el offset para la próxima solicitud
            offset += limit
    else:
        print(f"Error en la solicitud: {response.status_code}")
        has_more_reservations = False

# Crear una lista para almacenar los datos procesados
reservations_data = []

# Extraer y organizar los datos en la estructura deseada
for reservation in all_reservations:
    reservation_id = reservation.get('id')
    status = reservation.get('status')
    origin = reservation.get('origin', {}).get('channel')
    created = reservation.get('created')
    
    # Obtener el número de habitaciones reservadas
    num_rooms = len(reservation.get('rooms', []))

    total_price = reservation.get('price', {}).get('total')
    
    # Agregar los datos a la lista de reservas
    reservations_data.append({
        'id': reservation_id,
        'status': status,
        'origin': origin,
        'created': created,
        'dfrom': dfrom,
        'dto': dto,
        'total_price': total_price,
        'num_rooms': num_rooms  # Nueva variable: número de habitaciones reservadas
    })

# Crear un DataFrame a partir de los datos de las reservas
df = pd.DataFrame(reservations_data)
