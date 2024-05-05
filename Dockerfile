FROM python:3.12.0-bullseye
ENV PYTHONUNBUFFERED 1
ENV env dev
WORKDIR /app
ADD . /app
COPY requirements.txt /app/requirements.txt
EXPOSE 80
RUN pip install -r requirements.txt
RUN pre-commit
RUN apt update
RUN apt install git zsh curl nano wget -y
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" -y
RUN echo "zsh" >> ~/.bashrc
RUN sh -c "$(curl -fsSL https://deb.nodesource.com/setup_current.x)" -y
RUN apt install nodejs -y
RUN curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | tee /usr/share/keyrings/yarnkey.gpg >/dev/null
RUN echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt update && apt install yarn

RUN apt install libmemcached-dev -y
RUN pip install -r tests/requirements/py3.txt
# RUN npx puppeteer browsers install chrome