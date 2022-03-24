FROM python-base-image

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x main.py

CMD ["./run.sh"]
