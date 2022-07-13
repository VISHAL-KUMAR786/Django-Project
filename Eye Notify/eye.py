import datetime 
import time
from plyer import notification  
data = "Take 5 Second Rest to your 👀"
while(True):
    notification.notify(
        title= f" {data} "+"{}".format(datetime.date.today()),
        message="Relax you eye",
        timeout=50,
        app_icon= f"images.ico",
    )
    time.sleep(60*5)
