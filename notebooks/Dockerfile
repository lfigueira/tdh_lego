FROM jupyter/base-notebook

USER root

# Install all OS dependencies for fully functional notebook server
RUN apt-get update && apt-get install -yq --no-install-recommends \
    build-essential \
    emacs \
    git \
    inkscape \
    jed \
    libsm6 \
    libxext-dev \
    libxrender1 \
    lmodern \
    netcat \
    pandoc \
    python-dev \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-xetex \
    tzdata \
    unzip \
    nano \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /usr/app

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID

ADD ./requirements.txt ./
RUN pip install -r requirements.txt
ADD ./ ./

# hacky way to change permissions
USER root
RUN chown $NB_UID:users -R /usr/app
USER $NB_UID

ENTRYPOINT jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root
