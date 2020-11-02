FROM python:3.8

ADD ./ /

RUN pip install python-telegram-bot requests 

CMD [ "python3", "./bot.py" ]
