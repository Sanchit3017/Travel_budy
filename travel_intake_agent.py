import json
from typing import Dict, Any, Optional
from datetime import datetime
# from .base_agent import BaseAgent
# from src.models.database import SessionLocal
# from src.models.traveler import Traveler
# from src.models.trip import Trip, TravelMode, TripStatus

class TravelIntakeAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Travel Intake Agent",
            description="Captures and stores traveler information including destination, dates, and travel mode"
        )
    
    async def process(self, user_input: str, session_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.log_activity(f"Processing travel intake request from session {session_id}")
        
        try:
            if context and context.get('action') == 'store_trip':
                return await self.store_trip_data(context)
            else:
                return {
                    'agent': self.name,
                    'message': self._generate_intake_prompt(),
                    'requires_input': True,
                    'next_action': 'store_trip'
                }
        except Exception as e:
            self.log_activity(f"Error: {str(e)}")
            return {
                'agent': self.name,
                'error': str(e),
                'message': "I encountered an error while processing your travel information. Please try again."
            }
    
    def _generate_intake_prompt(self) -> str:
        return """Welcome to the Duty of Care Travel Assistant! I'll help you register your travel details.

To properly monitor your trip for any potential issues, I need the following information:

1. Your employee ID and name
2. Email address for notifications
3. Destination (country and city)
4. Travel dates (start and end date)
5. Mode of travel (flight, train, bus, car, etc.)
6. Purpose of travel (optional)

Please provide your travel details, and I'll register them in our system for monitoring."""
    
    async def store_trip_data(self, trip_data: Dict[str, Any]) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            traveler_data = trip_data.get('traveler', {})
            trip_info = trip_data.get('trip', {})
            
            traveler = db.query(Traveler).filter_by(
                employee_id=traveler_data.get('employee_id')
            ).first()
            
            if not traveler:
                traveler = Traveler(
                    employee_id=traveler_data.get('employee_id'),
                    name=traveler_data.get('name'),
                    email=traveler_data.get('email'),
                    phone=traveler_data.get('phone'),
                    company=traveler_data.get('company', 'Default Company'),
                    department=traveler_data.get('department')
                )
                db.add(traveler)
                db.flush()
                self.log_activity(f"Created new traveler: {traveler.name}")
            
            travel_mode_str = trip_info.get('travel_mode', 'other').upper()
            try:
                travel_mode = TravelMode[travel_mode_str]
            except KeyError:
                travel_mode = TravelMode.OTHER
            
            trip = Trip(
                traveler_id=traveler.id,
                destination=trip_info.get('destination'),
                destination_country=trip_info.get('destination_country'),
                destination_city=trip_info.get('destination_city'),
                start_date=datetime.strptime(trip_info.get('start_date'), '%Y-%m-%d').date(),
                end_date=datetime.strptime(trip_info.get('end_date'), '%Y-%m-%d').date(),
                travel_mode=travel_mode,
                status=TripStatus.PLANNED,
                purpose=trip_info.get('purpose'),
                notes=trip_info.get('notes')
            )
            db.add(trip)
            db.commit()
            
            self.log_activity(f"Stored trip {trip.id} for traveler {traveler.name} to {trip.destination}")
            
            return {
                'agent': self.name,
                'success': True,
                'trip_id': trip.id,
                'traveler_id': traveler.id,
                'message': f"""Travel details successfully registered!

Traveler: {traveler.name} ({traveler.email})
Destination: {trip.destination_city}, {trip.destination_country}
Travel Dates: {trip.start_date} to {trip.end_date}
Mode of Travel: {trip.travel_mode.value}

Your trip is now being monitored for any potential risks or disruptions. You'll receive notifications if any issues are detected."""
            }
        
        except Exception as e:
            db.rollback()
            self.log_activity(f"Database error: {str(e)}")
            raise
        finally:

            db.close()
