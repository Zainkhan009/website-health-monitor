# Website Health & Uptime Monitor

A Python-based application developed as an internship project for Internlytic Technologies. It automatically monitors website availability, response times, uptime history, downtime incidents, and performance issues.

## Features

- Automatic website monitoring every 60 seconds
- HTTP status code monitoring
- Website response time measurement
- SQLite database integration
- Uptime statistics and monitoring history
- Downtime incident tracking and duration calculation
- Automatic email alerts when a website goes DOWN
- Recovery email alerts when a website comes back UP
- Performance threshold monitoring (2000 ms)
- Slow performance email alerts
- Performance recovery notifications
- Docker containerization
- Docker Compose configuration
- Persistent database storage using Docker volumes

## Technologies Used

- Python 3.12
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
├── monitor_backup.py
├── history.py
├── stats.py
├── incidents.py
├── test_incidents.py
├── email_alerts.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── .env.example
├── packages/
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

4. Activate the environment.

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
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

Use a Gmail App Password for SMTP authentication.

**Never upload your real `.env` file to GitHub.**

## Run the Application

```bash
python monitor.py
```

The application checks configured websites every 60 seconds and stores monitoring results in SQLite.

## Docker Deployment

Make sure Docker and Docker Compose are installed.

Create and configure your `.env` file.

Build and start the application:

```bash
docker compose up -d --build
```

View application logs:

```bash
docker compose logs -f website-monitor
```

Check container status:

```bash
docker compose ps
```

Stop the container:

```bash
docker compose down
```

The application uses a named Docker volume to persist its database at:

```text
/app/data/monitor.db
```

Database data remains stored in the Docker volume when the container is recreated.

## Monitoring and Alerts

The application currently monitors:

- https://google.com
- https://github.com
- https://microsoft.com

It records HTTP status codes, response times, availability, and timestamps.

A response time above 2000 ms triggers a slow performance alert. When performance returns below the threshold, a recovery notification is sent.

Downtime incidents are recorded, and recovery notifications include the calculated downtime duration.

## Testing Email Alerts

Run the incident test:

```bash
python test_incidents.py
```

This test simulates a website going DOWN and recovering to UP.

It sends test downtime and recovery email notifications.

## Database

SQLite stores information in three main tables:

- `monitoring_history` — website checks and response times
- `incidents` — downtime incidents and duration
- `performance_incidents` — slow performance incidents and recovery

## Security

- Email credentials are stored in environment variables.
- The real `.env` file is excluded from Git.
- `.env.example` contains placeholder values only.

## Future Improvements

- Grafana monitoring dashboard
- Cloud deployment
- Advanced monitoring analytics

## Author

Developed as an internship project for Internlytic Technologies.

**Project:** Website Health & Uptime Monitor

**GitHub:** https://github.com/Zainkhan009/website-health-monitor