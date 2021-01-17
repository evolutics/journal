FROM python:3.8

RUN groupadd guest && useradd --create-home --gid guest guest
USER guest
WORKDIR /home/guest
ENV PATH="/home/guest/.local/bin:${PATH}"

COPY --chown=guest:guest . .
RUN pip install --no-cache-dir --requirement requirements.txt --user

CMD ["bash", "-c"]
