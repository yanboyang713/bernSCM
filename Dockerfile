FROM frolvlad/alpine-glibc:alpine-3.4

ARG CONDA_VERSION="py39_4.12.0"
ARG CONDA_SHA256="78f39f9bae971ec1ae7969f0516017f2413f17796670f7040725dd83fcff5689"
ARG CONDA_DIR="/opt/conda"

ENV PATH="$CONDA_DIR/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1

# Install conda
RUN echo "**** install dev packages ****" && \
    apk add --no-cache --virtual .build-dependencies bash ca-certificates wget && \
    \
    echo "**** get Miniconda ****" && \
    mkdir -p "$CONDA_DIR" && \
    wget "http://repo.continuum.io/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh" -O miniconda.sh && \
    echo "$CONDA_SHA256  miniconda.sh" | sha256sum -c && \
    \
    echo "**** install Miniconda ****" && \
    bash miniconda.sh -f -b -p "$CONDA_DIR" && \
    echo "export PATH=$CONDA_DIR/bin:\$PATH" > /etc/profile.d/conda.sh && \
    \
    echo "**** setup Miniconda ****" && \
    conda update --all --yes && \
    conda config --set auto_update_conda False && \
    \
    echo "**** cleanup ****" && \
    apk del --purge .build-dependencies && \
    rm -f miniconda.sh && \
    conda clean --all --force-pkgs-dirs --yes && \
    find "$CONDA_DIR" -follow -type f \( -iname '*.a' -o -iname '*.pyc' -o -iname '*.js.map' \) -delete && \
    \
    echo "**** finalize ****" && \
    mkdir -p "$CONDA_DIR/locks" && \
    chmod 777 "$CONDA_DIR/locks"

# install bash
RUN apk add --no-cache bash bash-doc bash-completion

# Install fortran
RUN apk add --no-cache bash bash-doc bash-completion
RUN apk add --no-cache musl-dev
RUN apk add --no-cache gfortran gdb make

# install notebook

# Make RUN commands use `bash --login`:
SHELL ["/bin/bash", "--login", "-c"]

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

RUN conda init bash
RUN bash -c "source /root/.bashrc"

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]
RUN ipython kernel install --user --name myenv --display-name "Python (myenv)"

WORKDIR /source

EXPOSE 8888
# ENTRYPOINT ["jupyter", "notebook","--allow-root","--ip=0.0.0.0","--port=8888","--no-browser"]

#jupyter notebook --ip='*' --NotebookApp.token='' --NotebookApp.password='' --allow-root
#ENTRYPOINT ["jupyter", "notebook","--allow-root","--ip=0.0.0.0","--port=8888","--no-browser"]
