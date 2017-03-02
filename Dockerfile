FROM ubuntu:14.04
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev postgresql-dev build-essential supervisor
ADD . .
RUN pip install -r ./requirements.txt

# This is to protect against load balancer keep-alive timeouts; see
# https://github.com/benoitc/gunicorn/issues/1194 and
# https://serverfault.com/questions/782022/keepalive-setting-for-gunicorn-behind-elb-without-nginx
ENV PYTHONUNBUFFERED 1

CMD ["/usr/bin/supervisord", "-c", "supervisord.conf"]
