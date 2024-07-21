from notificationapi_python_server_sdk import notificationapi



async def send_notification(clientId:str, clientSecret:str,user,notification):
    print("Sending Notification..")
    notificationapi.init(
        clientId ,  # clientId
        clientSecret# clientSecret
    )

    await notificationapi.send({
        "notificationId": notification["notification_id"],
        "user": {
          "id": user["email"],
          "email": user["email"],
          "number": user["number"] # Replace with your phone number
        },
        "mergeTags": {
          "user": {
                    "firstName": user["full_name"]
          },
          "order_id": notification["order_id"]
        }
    })

