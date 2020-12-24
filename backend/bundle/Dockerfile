# use python 3.8 base image
FROM python:3.8

# specify working directory
WORKDIR /code

ENV GRAPHERY_EXECUTOR_DEFAULT_SERVE_URL="0.0.0.0"
EXPOSE 7590 7590

# make cache folder
RUN mkdir /code/graphery_cache
ENV CONTROLLER_CACHE_PATH="/code/graphery_cache"

# copy src
ADD ./bundle /code/bundle/
ADD ./user_server.py /code

# run command
CMD ["python", "/code/user_server.py"]
