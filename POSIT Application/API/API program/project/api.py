import requests


files = {'input_file': open('input.zip','rb')}
r = requests.post("http://django-env.qqhswtcpb3.us-west-2.elasticbeanstalk.com/api_posit", files=files)
print(r.text)
