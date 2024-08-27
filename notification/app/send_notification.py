from notificationapi_python_server_sdk import notificationapi


async def order_notifications(clientId:str, clientSecret:str,message:dict):
    print("Sending Notification..")
    notificationapi.init(
        clientId ,  # clientId
        clientSecret# clientSecret
    )
    # print("callled-----------------------------------------------")
    await notificationapi.send({
        "notificationId": message["notification"]["notification_id"],
        "user": {
          "id": message["user"]["email"],
          "email": message["user"]["email"],
          "number": "+15005550006" # Replace with your phone number
        },
        "mergeTags": {
          "full_name":message["user"]["full_name"],
          "order_id": message["notification"]["order_id"],
          "commentId": "testCommentId"
        }
    })
    # print("Notification Sent")
   

async def user_notifications(clientId:str, clientSecret:str,message:dict):
    print("Sending Notification..")
    notificationapi.init(
        clientId ,  # clientId
        clientSecret# clientSecret
    )
    
    if message["event"]=="user_registered":
      await notificationapi.send({
          "notificationId": "new_account",
          "user": {
            "id": message["email"],
            "email": message["email"],
            "number": "+15005550006" # Replace with your phone number
          },
          "mergeTags": {
            "full_name": message["full_name"],
            "comment": "Thanks for registering with us",
            "commentId": "testCommentId"
          }
      })

    if message["event"]=="user_updated" or message["event"]=="user_password_changed":
      await notificationapi.send({
        "notificationId": "account_update",
        "user": {
          "id": message["email"],
            "email": message["email"],
          "number": "+15005550006" # Replace with your phone number
        },
        "mergeTags": {
          "full_name": message["full_name"],
          "comment": "Your account has been updated",
          "commentId": "testCommentId"
        }
    })
      
    print("Notification Sent")
        

