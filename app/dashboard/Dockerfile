FROM python:3.9.0

# Maintainer of the Dockerfile
LABEL maintainer="Alejandro Aceituna Cano - dev@aacecan.com"

# Input data
ARG NON_ROOT_USER=nroot
ARG ID=1000

# Hadolint DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Change directory to /tmp to do administrative tasks
WORKDIR /tmp

# Create a non-root user group
RUN addgroup ${NON_ROOT_USER} --gid ${ID} && \
    adduser \
      --disabled-password \
      --uid ${ID} --gid ${ID} \
      --shell /bin/bash \
      --gecos "" \
      ${NON_ROOT_USER}

# Upgrade OS && install all OS dependencies
RUN apt-get update && \
      DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
        wkhtmltopdf && \
    # Add non-root python bin to PATH
    echo "export PATH=/home/${NON_ROOT_USER}/.local/bin:${PATH}" >> /etc/bash.bashrc && \
    # APT and /tmp cleanup
    apt-get clean && apt-get autoremove -y && \
        rm -rf /var/lib/{apt,dpkg,cache,log}/ && \
        rm -rf -- *

# Change directory to /app to execute the app
WORKDIR /app

# Change the ownership of /app to the non-root user
RUN chown -R ${NON_ROOT_USER}:${NON_ROOT_USER} /app

# Install python libraries
COPY ./requirements.txt /app
RUN pip install --upgrade pip==21.3.1 --no-cache-dir && \
    pip install -r /app/requirements.txt --no-cache-dir

# Add local files as late as possible to avoid cache busting
COPY --chown=${NON_ROOT_USER}:${NON_ROOT_USER} ./ /app

# Use non-root user
USER ${NON_ROOT_USER}

ENTRYPOINT [ "streamlit", "run"]
CMD ["main.py"]
