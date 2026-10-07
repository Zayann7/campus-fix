# Python Flask Docker App

**CLOUD NATION** &mdash; Docker Class | Created by Mohammed Mubashir
WhatsApp: +91 78878 01551 | Email: cloudnation46@gmail.com

A small Python (Flask) web application packaged as a Docker image.

## Run it on your EC2 (Amazon Linux) machine

```bash
sudo yum install git -y
git clone https://github.com/WorkspaceCN/python-flask-docker-app.git
cd python-flask-docker-app
docker build -t python-flask-app .
docker run -d -p 5000:5000 python-flask-app
```

Open in the browser: `http://<EC2-public-ip>:5000/`

Remember to open the port in the EC2 **Security Group** (Inbound rule, Custom TCP, Anywhere IPv4).

---
*Cloud Nation: learn, practise, get hired.*
