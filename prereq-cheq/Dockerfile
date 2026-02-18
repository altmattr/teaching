FROM openjdk:11

WORKDIR /working

RUN apt-get update
RUN apt-get install -y git vim
RUN apt-get install -y firebase

COPY .vimrc /root/.vimrc
COPY .vim /root/.vim
COPY .ssh /root/.ssh
RUN git config --global user.email "alt.mattr@gmail.com"
RUN git config --global user.name "Matt Roberts"

ENV TERM=xterm-256color
RUN echo 'export PS1="\[\e[38;5;251m\]\u@$TAG \w > \[\e[0m\]"' >> /root/.bashrc

CMD [ "bash" ]
