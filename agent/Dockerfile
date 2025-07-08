FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
        xvfb \
        x11vnc \
        fluxbox \
        xdotool \
        wget \
        supervisor \
        python3 \
        python3-pip \
        git \
        curl \
        unzip

# Install Node.js 18 (official setup script)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install create-react-app (compatible with Node 18's default npm)
RUN npm install -g create-react-app

# Install noVNC
RUN mkdir -p /opt/novnc && \
    wget -qO- https://github.com/novnc/noVNC/archive/refs/tags/v1.3.0.tar.gz | tar xz -C /opt/novnc --strip 1

# Install Jupyter
RUN pip3 install notebook

# Create workspace
RUN mkdir /workspace
WORKDIR /workspace

# Copy supervisor config and agent scripts
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY agent_start.sh /workspace/agent_start.sh
COPY context_manager.py /workspace/context_manager.py

# Make scripts executable
RUN chmod +x /workspace/agent_start.sh

# Expose ports: VNC, noVNC, Jupyter
EXPOSE 5900 6080 8888

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]