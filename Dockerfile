FROM heroku/miniconda

# Grab requirements.txt.
ADD requirements.txt 

# Install dependencies
RUN pip install -qr requirements.txt

# Add our code
#ADD ./webapp /opt/webapp/
#WORKDIR /opt/webapp

RUN conda install scikit-learn
RUN conda install rdkit

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
