# Website Health & Uptime Monitor

A Python-based application that automatically monitors website availability, response times, uptime history, and downtime incidents.

## Features

- Automatic website monitoring every 60 seconds
- HTTP status code monitoring
- Website response time measurement
- SQLite database integration
- Uptime statistics and monitoring history
- Downtime incident tracking
- Automatic email alerts when a website goes DOWN
- Recovery email alerts when a website comes back UP
- Docker containerization
- Docker Compose configuration

## Technologies Used

- Python
- HTTPX
- SQLite
- Python-dotenv
- Docker
- Docker Compose
- Gmail SMTP

## Project Structure

```text
website-health-monitor/
│
├── monitor.py
├── history.py
├── stats.py
├── incidents.py
├── email_alerts.py
├── test_incidents.py
├── monitor_backup.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── .env.example
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Zainkhan009/website-health-monitor.git
```

2. Open the project directory:

```bash
cd website-health-monitor
```

3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate the environment:

Windows:

```bash
.venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

## Email Configuration

Create a `.env` file in the project root using `.env.example`.

Add your Gmail credentials:

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ALERT_EMAIL=receiver@gmail.com
```

Never upload your real `.env` file to GitHub.

## Run the Application

```bash
python monitor.py
```

The application checks selected websites every 60 seconds and stores monitoring results in SQLite.

## Docker Deployment

Build and start the container:

```bash
docker compose up --build -d
```

View application logs:

```bash
docker compose logs -f
```

Stop the container:

```bash
docker compose down
```

Make sure Docker is running and the `.env` file is configured before starting the container.

## Database

SQLite stores:

- Website monitoring history
- HTTP status codes
- Response times
- Website availability
- Downtime incidents
- Incident duration

## Email Alerts

The application sends email notifications when a monitored website goes DOWN and when it recovers.

## Future Improvements

- Performance threshold alerts
- Grafana monitoring dashboard
- Cloud deployment
- Advanced monitoring analytics

## Author

Developed as an internship project for Internlytic Technologies.

**Project:** Website Health & Uptime Monitor