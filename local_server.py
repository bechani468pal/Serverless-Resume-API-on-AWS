import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configure local AWS SDK settings
os.environ.setdefault("AWS_DEFAULT_REGION", "ap-south-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "local")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "local")

from src import lambda_function

# Load resume JSON
RESUME_FILE = "src/resume.json"

with open(RESUME_FILE, "r", encoding="utf-8") as file:
    resume_data = json.load(file)


# Simulate DynamoDB locally
class LocalDynamoDB:

    def get_item(self, Key):
        section = Key["SK"].lower()

        if section in resume_data:
            return {
                "Item": {
                    "PK": "RESUME",
                    "SK": Key["SK"],
                    "data": resume_data[section]
                }
            }

        return {}

    def query(self, **kwargs):
        items = []

        for section, data in resume_data.items():
            items.append({
                "PK": "RESUME",
                "SK": section.upper(),
                "data": data
            })

        return {"Items": items}


# Connect local database simulator
lambda_function.table = LocalDynamoDB()


class ResumeAPIHandler(BaseHTTPRequestHandler):

    API_KEY = "demo-resume-key"

    def check_api_key(self):
        return self.headers.get("x-api-key") == self.API_KEY

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, x-api-key")
        self.end_headers()

    def do_GET(self):

        if not self.check_api_key():
            self.send_json(403, {"error": "Invalid or missing API key"})
            return

        event = {
            "rawPath": self.path.split("?")[0]
        }

        result = lambda_function.lambda_handler(event, None)
        body = json.loads(result["body"])

        self.send_json(result["statusCode"], body)

    def do_POST(self):

        if not self.check_api_key():
            self.send_json(403, {"error": "Invalid or missing API key"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))

            if content_length <= 0 or content_length > 1_000_000:
                self.send_json(400, {"error": "Invalid request size"})
                return

            body = self.rfile.read(content_length)
            submitted_data = json.loads(body.decode("utf-8"))

            if not isinstance(submitted_data, dict):
                self.send_json(400, {"error": "JSON object required"})
                return

            allowed_sections = {
                "personal",
                "experience",
                "education",
                "skills"
            }

            if not submitted_data or not set(submitted_data).issubset(allowed_sections):
                self.send_json(400, {"error": "Invalid resume sections"})
                return

            for section, data in submitted_data.items():
                if section == "personal" and not isinstance(data, dict):
                    self.send_json(400, {"error": "Personal details must be an object"})
                    return

                if section in ("experience", "education", "skills") and not isinstance(data, list):
                    self.send_json(400, {"error": f"{section} must be a list"})
                    return

            # Update resume data
            resume_data.update(submitted_data)

            # Save changes to JSON file
            with open(RESUME_FILE, "w", encoding="utf-8") as file:
                json.dump(resume_data, file, indent=2, ensure_ascii=False)

            self.send_json(200, {
                "message": "Resume saved successfully",
                "resume": resume_data
            })

        except json.JSONDecodeError:
            self.send_json(400, {"error": "Invalid JSON data"})

        except Exception as error:
            print("Error:", str(error))
            self.send_json(500, {"error": "Could not save resume"})

    def send_json(self, status, data):

        response = json.dumps(data, default=str).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, x-api-key")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

        self.wfile.write(response)

    def log_message(self, format, *args):
        print("[API]", format % args)


server = HTTPServer(("127.0.0.1", 8000), ResumeAPIHandler)

print("====================================")
print(" SERVERLESS RESUME API")
print("====================================")
print("Server: http://127.0.0.1:8000")
print("API Key: demo-resume-key")
print("GET and POST enabled")
print("Server is running...")
print("Press CTRL+C to stop.")

server.serve_forever()