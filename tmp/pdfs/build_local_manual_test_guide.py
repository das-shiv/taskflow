from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Preformatted,
    Table,
    TableStyle,
)


OUTPUT = "output/pdf/taskflow_local_manual_test_guide.pdf"


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleBlock",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=29,
        textColor=colors.HexColor("#172026"),
        spaceAfter=12,
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#136f63"),
        spaceBefore=14,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="Subsection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#22313a"),
        spaceBefore=9,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.4,
        leading=13,
        textColor=colors.HexColor("#26343b"),
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor("#4f6571"),
        spaceAfter=5,
    )
)


def code(text):
    return Preformatted(
        text.strip("\n"),
        ParagraphStyle(
            name="Code",
            fontName="Courier",
            fontSize=6.8,
            leading=8.5,
            textColor=colors.HexColor("#1b262c"),
            backColor=colors.HexColor("#f2f5f6"),
            borderColor=colors.HexColor("#d9e1e4"),
            borderWidth=0.5,
            borderPadding=6,
            leftIndent=0,
            rightIndent=0,
            spaceBefore=3,
            spaceAfter=8,
        ),
    )


def p(text):
    return Paragraph(text, styles["Body"])


def small(text):
    return Paragraph(text, styles["Small"])


def heading(text):
    return Paragraph(text, styles["Section"])


def subheading(text):
    return Paragraph(text, styles["Subsection"])


story = []

story.append(Paragraph("TaskFlow Local Manual Test Guide", styles["TitleBlock"]))
story.append(
    p(
        "Step-by-step Ubuntu commands to run the TaskFlow setup locally without creating Docker containers, Docker images, Kubernetes manifests, or DevOps assets."
    )
)
story.append(
    small(
        "Assumptions: you are on Ubuntu 22.04 or 24.04, the project lives at ~/taskflow or another local path, and required packages are not installed yet. Replace paths and passwords only where noted."
    )
)

overview = [
    ["Component", "Local port", "Purpose"],
    ["PostgreSQL", "5432", "Persistent storage for task-service and notification-service"],
    ["Redis", "6379", "Task read cache for task-service"],
    ["Kafka", "9092", "Task event broker"],
    ["task-service", "8080", "Spring Boot REST API"],
    ["notification-service", "8081", "Kafka consumer and notification recorder"],
    ["frontend", "5173", "React UI"],
]
table = Table(overview, colWidths=[1.45 * inch, 0.85 * inch, 4.0 * inch])
table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#136f63")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.2),
            ("LEADING", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cad4d8")),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#fbfcfc")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )
)
story.append(Spacer(1, 8))
story.append(table)

story.append(heading("1. Install Required Packages"))
story.append(p("Install Java 21, Maven, Node.js, npm, PostgreSQL, Redis, curl, jq, and helper tools."))
story.append(
    code(
        """
sudo apt update
sudo apt install -y openjdk-21-jdk maven postgresql postgresql-contrib redis-server \\
  curl jq wget tar ca-certificates gnupg lsb-release

java -version
mvn -version
node -v || true
npm -v || true
psql --version
redis-server --version
"""
    )
)
story.append(
    p(
        "If Node.js is missing or too old, install the current LTS from NodeSource. This project was verified with modern Node 20+ behavior."
    )
)
story.append(
    code(
        """
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node -v
npm -v
"""
    )
)

story.append(heading("2. Install Kafka Locally"))
story.append(p("Install Kafka into /opt/kafka and create a convenience symlink. This runs directly on your host, not in Docker."))
story.append(
    code(
        """
cd /tmp
wget https://archive.apache.org/dist/kafka/3.9.0/kafka_2.13-3.9.0.tgz
sudo tar -xzf kafka_2.13-3.9.0.tgz -C /opt
sudo ln -sfn /opt/kafka_2.13-3.9.0 /opt/kafka
sudo chown -R "$USER":"$USER" /opt/kafka_2.13-3.9.0
/opt/kafka/bin/kafka-storage.sh --help >/dev/null
"""
    )
)

story.append(heading("3. Prepare The Project Directory"))
story.append(p("Move into your TaskFlow project root. Adjust this path if you cloned or copied it elsewhere."))
story.append(
    code(
        """
cd ~/taskflow

# Quick structure check
ls
ls frontend task-service notification-service database devops docs

# devops should exist but remain empty for now
find devops -mindepth 1 -maxdepth 1 -print
"""
    )
)

story.append(PageBreak())
story.append(heading("4. Start PostgreSQL And Create Databases"))
story.append(p("Start PostgreSQL, create an application user, and create separate databases for the two services."))
story.append(
    code(
        """
sudo systemctl enable --now postgresql
sudo systemctl status postgresql --no-pager

sudo -u postgres psql <<'SQL'
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'taskflow') THEN
    CREATE ROLE taskflow LOGIN PASSWORD 'taskflow';
  END IF;
END
$$;
SQL

sudo -u postgres createdb -O taskflow taskflow || true
sudo -u postgres createdb -O taskflow taskflow_notifications || true

PGPASSWORD=taskflow psql -h localhost -U taskflow -d taskflow -c "select current_database();"
PGPASSWORD=taskflow psql -h localhost -U taskflow -d taskflow_notifications -c "select current_database();"
"""
    )
)

story.append(heading("5. Start Redis"))
story.append(p("Run Redis as a normal Ubuntu service and verify that it responds."))
story.append(
    code(
        """
sudo systemctl enable --now redis-server
sudo systemctl status redis-server --no-pager
redis-cli ping
"""
    )
)

story.append(PageBreak())
story.append(heading("6. Start Kafka In KRaft Mode"))
story.append(
    p(
        "Open a dedicated terminal for Kafka. The commands below format a local Kafka data directory once, then start the broker."
    )
)
story.append(
    code(
        """
mkdir -p ~/taskflow-runtime/kafka-logs

KAFKA_CLUSTER_ID="$(/opt/kafka/bin/kafka-storage.sh random-uuid)"
/opt/kafka/bin/kafka-storage.sh format \\
  -t "$KAFKA_CLUSTER_ID" \\
  -c /opt/kafka/config/kraft/server.properties \\
  --ignore-formatted

/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/kraft/server.properties
"""
    )
)
story.append(p("In another terminal, create and verify the task event topic."))
story.append(
    code(
        """
/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 \\
  --create --if-not-exists --topic task-events --partitions 1 --replication-factor 1

/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
"""
    )
)

story.append(heading("7. Run task-service"))
story.append(p("Open a new terminal from the project root and start the REST API. Flyway will create the tasks table."))
story.append(
    code(
        """
cd ~/taskflow/task-service

export SERVER_PORT=8080
export SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/taskflow
export SPRING_DATASOURCE_USERNAME=taskflow
export SPRING_DATASOURCE_PASSWORD=taskflow
export SPRING_DATA_REDIS_HOST=localhost
export SPRING_DATA_REDIS_PORT=6379
export SPRING_KAFKA_BOOTSTRAP_SERVERS=localhost:9092
export TASKFLOW_KAFKA_TASK_EVENTS_TOPIC=task-events

mvn spring-boot:run
"""
    )
)
story.append(p("Health check from a separate terminal:"))
story.append(
    code(
        """
curl -s http://localhost:8080/actuator/health | jq
curl -s http://localhost:8080/actuator/prometheus | head
"""
    )
)

story.append(heading("8. Run notification-service"))
story.append(
    p(
        "Open another terminal from the project root and start the Kafka consumer. Flyway will create the notifications table."
    )
)
story.append(
    code(
        """
cd ~/taskflow/notification-service

export SERVER_PORT=8081
export SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/taskflow_notifications
export SPRING_DATASOURCE_USERNAME=taskflow
export SPRING_DATASOURCE_PASSWORD=taskflow
export SPRING_KAFKA_BOOTSTRAP_SERVERS=localhost:9092
export TASKFLOW_KAFKA_TASK_EVENTS_TOPIC=task-events

mvn spring-boot:run
"""
    )
)
story.append(p("Health check from a separate terminal:"))
story.append(
    code(
        """
curl -s http://localhost:8081/actuator/health | jq
curl -s http://localhost:8081/actuator/prometheus | head
"""
    )
)

story.append(heading("9. Run The Frontend"))
story.append(p("Open another terminal and start the React app."))
story.append(
    code(
        """
cd ~/taskflow/frontend

export VITE_TASK_API_BASE_URL=http://localhost:8080
npm install
npm run dev
"""
    )
)
story.append(p("Open the UI at http://localhost:5173."))

story.append(heading("10. End-To-End API Smoke Test"))
story.append(p("Create a task, list tasks, complete the task, then confirm that notification-service recorded Kafka events."))
story.append(
    code(
        """
TASK_ID="$(curl -s -X POST http://localhost:8080/api/tasks \\
  -H 'Content-Type: application/json' \\
  -d '{"title":"Manual local E2E","description":"PostgreSQL Redis Kafka Spring React"}' \\
  | jq -r '.id')"

echo "$TASK_ID"

curl -s http://localhost:8080/api/tasks | jq

curl -s -X PATCH "http://localhost:8080/api/tasks/${TASK_ID}/complete" | jq

sleep 3

PGPASSWORD=taskflow psql -h localhost -U taskflow -d taskflow \\
  -c "select id, title, status, created_at, completed_at from tasks order by created_at desc limit 5;"

PGPASSWORD=taskflow psql -h localhost -U taskflow -d taskflow_notifications \\
  -c "select task_id, event_type, status, received_at from notifications order by received_at desc limit 10;"
"""
    )
)

story.append(heading("11. Run Automated Tests"))
story.append(p("Run the project tests locally. Backend tests require Maven; frontend tests require npm dependencies."))
story.append(
    code(
        """
cd ~/taskflow/task-service
mvn test

cd ~/taskflow/notification-service
mvn test

cd ~/taskflow/frontend
npm test
npm run build
"""
    )
)

story.append(heading("12. Optional Manual Kafka Inspection"))
story.append(p("Watch task events directly from Kafka while you create or complete tasks."))
story.append(
    code(
        """
/opt/kafka/bin/kafka-console-consumer.sh \\
  --bootstrap-server localhost:9092 \\
  --topic task-events \\
  --from-beginning
"""
    )
)

story.append(heading("13. Clean Shutdown"))
story.append(p("Stop app terminals with Ctrl+C. Then stop host services if you no longer need them."))
story.append(
    code(
        """
sudo systemctl stop redis-server
sudo systemctl stop postgresql

# Stop Kafka with Ctrl+C in the Kafka terminal.
"""
    )
)

story.append(heading("14. Troubleshooting Checklist"))
story.append(
    code(
        """
# Port checks
ss -ltnp | grep -E ':5432|:6379|:9092|:8080|:8081|:5173'

# PostgreSQL connection
PGPASSWORD=taskflow psql -h localhost -U taskflow -d taskflow -c '\\dt'

# Redis connection
redis-cli ping

# Kafka topic state
/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic task-events

# Spring health endpoints
curl -s http://localhost:8080/actuator/health | jq
curl -s http://localhost:8081/actuator/health | jq

# If Kafka data is corrupted during practice, stop Kafka and reset local logs
rm -rf /tmp/kraft-combined-logs ~/taskflow-runtime/kafka-logs
"""
    )
)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#6c7c84"))
    canvas.drawString(inch * 0.65, 0.45 * inch, "TaskFlow local manual test guide")
    canvas.drawRightString(A4[0] - inch * 0.65, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=0.55 * inch,
    leftMargin=0.55 * inch,
    topMargin=0.55 * inch,
    bottomMargin=0.65 * inch,
    title="TaskFlow Local Manual Test Guide",
    author="Codex",
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
