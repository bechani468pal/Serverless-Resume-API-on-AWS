import json
import boto3
import os

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ.get("RESUME_TABLE", "ResumeData")
table = dynamodb.Table(TABLE_NAME)


def load_resume_data():

    # Read resume JSON file
    file_path = os.path.join(
        os.path.dirname(__file__),
        "resume.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        resume = json.load(file)

    # Store each section in DynamoDB
    for section, data in resume.items():

        item = {
            "PK": "RESUME",
            "SK": section.upper(),
            "data": data
        }

        table.put_item(Item=item)

        print(f"Uploaded {section} successfully!")

    print("Resume data uploaded successfully!")


if __name__ == "__main__":
    load_resume_data()
    