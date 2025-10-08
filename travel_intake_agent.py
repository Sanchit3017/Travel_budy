from typing import Dict, Any
from datetime import datetime


def process_travel_intake(user_input: Dict[str, Any]) -> Dict[str, Any]:
    
    try:
        traveler_info = user_input.get('traveler', {})
        trip_info = user_input.get('trip', {})
        
       
        required_traveler = ['user_id', 'name', 'email']
        required_trip = ['destination_country', 'destination_city', 'start_date', 'end_date', 'travel_mode']
        
        missing = []
        for field in required_traveler:
            if not traveler_info.get(field):
                missing.append(f'traveler.{field}')
        
        for field in required_trip:
            if not trip_info.get(field):
                missing.append(f'trip.{field}')
        
        if missing:
            return {
                'success': False,
                'error': f"Missing required fields: {', '.join(missing)}"
            }
        
      
        try:
            start_dt = datetime.strptime(trip_info['start_date'], '%d-%m-%Y')
            end_dt = datetime.strptime(trip_info['end_date'], '%d-%m-%Y')
            
            if end_dt < start_dt:
                return {
                    'success': False,
                    'error': 'End date cannot be before start date'
                }
        except ValueError:
            return {
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }
        
        # build confirmation response
        confirmation = {
            'success': True,
            'traveler': {
                'user_id': traveler_info['user_id'],
                'name': traveler_info['name'],
                'email': traveler_info['email'],
                'phone': traveler_info.get('phone', 'Not provided'),
                'company': traveler_info.get('company', 'Not provided'),
                'department': traveler_info.get('department', 'Not provided')
            },
            'trip': {
                'destination': f"{trip_info['destination_city']}, {trip_info['destination_country']}",
                'destination_city': trip_info['destination_city'],
                'destination_country': trip_info['destination_country'],
                'start_date': trip_info['start_date'],
                'end_date': trip_info['end_date'],
                'travel_mode': trip_info['travel_mode'],
                'purpose': trip_info.get('purpose', 'Not specified'),
                'notes': trip_info.get('notes', '')
            },
            'message': f"""Travel details confirmed!

Traveler: {traveler_info['name']} ({traveler_info['email']})
Destination: {trip_info['destination_city']}, {trip_info['destination_country']}
Travel Dates: {trip_info['start_date']} to {trip_info['end_date']}
Mode of Travel: {trip_info['travel_mode']}

Your trip registration is complete."""
        }
        
        return confirmation
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error processing travel intake: {str(e)}'
        }



