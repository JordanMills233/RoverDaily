from datetime import datetime, timedelta
from twitter import Twitter, OAuth
from datetime import date, timedelta
import requests
import json 
import shutil
import config

today = date.today()
yesterday = today - timedelta(days=365)
print("Today's date:", today)
print("1 Year ago date:", yesterday)

key = config.NasaKey

r = requests.get('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={}&api_key={}'.format(yesterday, key))
a = r.url

response = json.loads(requests.get(a).text)

t = response['photos'][000]['img_src']

## Set up the image URL and filename
image_url = t
filename = 'dailyimage.jpg'

# Open the url image, set stream to True, this will return the stream content.
r = requests.get(image_url, stream = True)

# Check if the image was retrieved successfully
if r.status_code == 200:
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    r.raw.decode_content = True
    
    # Open a local file with wb ( write binary ) permission.
    with open(filename,'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    print('Image sucessfully Downloaded:',filename)
else:
    print('Image Couldn\'t be retreived')


consumer_key = config.consumer_key
consumer_secret_key = config.consumer_secret_key
access_token = config.access_token
access_token_secret = config.access_token_secret


if __name__ == '__main__':
    my_auth = OAuth(token=access_token,
                    token_secret=access_token_secret,
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret_key)

    t = Twitter(auth=my_auth)

    # Send images along with your tweets:
    # - first just read images from the web or from files the regular way:
    with open("dailyimage.jpg", "rb") as imagefile:
        imagedata = imagefile.read()
    # - then upload medias one by one on Twitter's dedicated server
    #   and collect each one's id:
    t_up = Twitter(domain='upload.twitter.com', auth=my_auth)
    id_img = t_up.media.upload(media=imagedata)["media_id_string"]
    t.statuses.update(status="Curiosity rover {}".format(yesterday),
                      media_ids=",".join([id_img]))



