import requests


files = {'files': open('webpage3.txt','rb')}
r = requests.post("http://django-env.qqhswtcpb3.us-west-2.elasticbeanstalk.com/api_posit", files=files)
print(r.text)
