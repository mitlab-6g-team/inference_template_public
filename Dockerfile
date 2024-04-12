FROM {base_image_name}
ENV PYTHONUNBUFFERED 1
RUN mkdir /inference_host
WORKDIR /inference_host
COPY . /inference_host

RUN pip install -r ./requirements/base.txt

EXPOSE 30305
CMD python3 manage.py runserver 0.0.0.0:30305
