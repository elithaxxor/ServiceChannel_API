import json

json_string = """
{
    "Action": "UPDATE",
    "EventType": "WorkOrderStarRemoved",
    "Object": {
        "Category": "REPAIR",
        "Id": 275863375,
        "LocationId": 2006301252,
        "ProviderId": 2098457598,
        "SubscriberId": 2014917340,
        "Trade": "FACADE",
        "UpdatedBy": {
            "AuthUserId": 38135,
            "Email": "fuad@dedicatedglass.com",
            "FullName": "",
            "Id": 4425509,
            "ProviderId": 2098457598,
            "UserName": "fuad@dedicatedglass.com"
        },
        "UpdatedDate_DTO": "2024-04-26T19:09:06.6394621-04:00"
    },
    "Type": "WoRootNotification",
    "Version": 1
}
"""

python_dict = json.loads(json_string)
print(python_dict)