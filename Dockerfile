FROM ubuntu:14.04
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt-get install -y libpq-dev
ADD . .
RUN pip3 install -r ./requirements.txt
RUN pip3 install honcho

# This is to protect against load balancer keep-alive timeouts; see
# https://github.com/benoitc/gunicorn/issues/1194 and
# https://serverfault.com/questions/782022/keepalive-setting-for-gunicorn-behind-elb-without-nginx
ENV PYTHONUNBUFFERED 1

CMD honcho run ./debug.py
