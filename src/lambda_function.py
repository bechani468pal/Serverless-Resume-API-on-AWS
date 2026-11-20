import json
import os
import boto3

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("RESUME_TABLE", "ResumeData")
table = dynamodb.Table(TABLE_NAME)


def response(status_code, data):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(data, default=str)
    }


def lambda_handler(event, context):

    try:
        path = event.get("rawPath") or event.get("path", "/resume")

        endpoint = path.rstrip("/").split("/")[-1].lower()

        # Map API endpoints to DynamoDB sort keys
        sections = {
            "personal": "PERSONAL",
            "experience": "EXPERIENCE",
            "education": "EDUCATION",
            "skills": "SKILLS"
        }

        # Retrieve complete resume
        if endpoint == "resume":
            result = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key("PK").eq("RESUME")
            )

            resume_data = {}

            for item in result.get("Items", []):
                section = item["SK"].lower()
                resume_data[section] = item["data"]

            return response(200, {
                "message": "Complete resume retrieved successfully",
                "resume": resume_data
            })

        # Retrieve individual resume section
        if endpoint in sections:

            result = table.get_item(
                Key={
                    "PK": "RESUME",
                    "SK": sections[endpoint]
                }
            )

            item = result.get("Item")

            if not item:
                return response(404, {
                    "error": "Resume section not found"
                })

            return response(200, {
                "section": endpoint,
                "data": item["data"]
            })

        return response(404, {
            "error": "Invalid API endpoint"
        })

    except Exception as error:
        print("Error:", str(error))

        return response(500, {
            "error": "Internal server error"
        })
    