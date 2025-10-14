from agentcore import AgentCore, AgentCoreConfig
import boto3, os, requests

# Initialize AWS services
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Travels_Care')

TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')


# Initialize AgentCore runtime
core = AgentCore(AgentCoreConfig(name="TravelMonitoringCore"))

@core.tool("register_trip", description="Register a new trip for monitoring.")
def register_trip(payload):
    emp_id = payload["emp_id"]
    trip_id = payload["trip_id"]
    dest = payload["destination"]
    start_date = payload["start_date"]
    end_date = payload["end_date"]

    table.put_item(Item={
        "EmpID": emp_id,
        "TripID": trip_id,
        "Destination": dest,
        "StartDate": start_date,
        "EndDate": end_date,
        "MonitoringStatus": "Active"
    })
    return {"message": f"Trip {trip_id} to {dest} registered successfully"}

@core.tool("monitor_trip", description="Check weather for active trip and raise alert.")
def monitor_trip(payload):
    dest = payload["destination"]
    trip_id = payload["trip_id"]

    url = f"http://api.openweathermap.org/data/2.5/weather?q={dest}&appid={ac97dac371f79c3b0030d363ce9d336c}"
    r = requests.get(url, timeout=8)
    data = r.json()
    weather = data["weather"][0]["main"]

    if weather.lower() in ["rain", "storm", "snow", "extreme"]:
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="Travel Alert",
            Message=f"⚠️ Alert for {dest}: {weather}"
        )
        return {"status": "Alert Sent", "weather": weather}
    else:
        return {"status": "OK", "weather": weather}

if __name__ == "__main__":
    core.run(host="0.0.0.0", port=8080)
