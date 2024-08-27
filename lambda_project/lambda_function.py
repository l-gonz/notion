import json
import os
import logging
from notion_client import Client
import requests

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment variables
NOTION_API_TOKEN = os.getenv('NOTION_API_TOKEN')
SLACK_VERIFICATION_TOKEN = os.getenv('SLACK_VERIFICATION_TOKEN')

# Initialize Notion client
notion = Client(auth=NOTION_API_TOKEN)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        slack_token = body.get('token')
        event_type = body.get('type')

        if slack_token != SLACK_VERIFICATION_TOKEN:
            return invalid_token_response()

        if event_type == 'url_verification':
            return answer_challenge_response()
        elif event_type == 'event_callback':
            return handle_event_callback(body)
        else:
            return unknown_event_response()

    except Exception as e:
        return generic_error_response(e)


def handle_event_callback(body):

    database_id, page_id = parse_event_text(body)
    update_notion_task(database_id, page_id)

    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'success'})
    }

def parse_event_text():
    event_data = body.get('event', {})
    message_text = event_data.get('text', '')

    # Log the incoming Slack message
    logger.info(f"Received Slack event: {message_text}")

    # Extract Notion Database ID and Page ID from the message
    links = [word for word in message_text.split() if word.startswith("https://www.notion.so")]
    if len(links) < 2:
        logger.error("Not enough Notion links found in the message.")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Notion links missing'})
        }

    database_url = links[0]
    page_url = links[1]

    # Extract IDs from the URLs
    database_id = database_url.split('-')[-1]
    page_id = page_url.split('-')[-1]

    logger.info(f"Database ID: {database_id}, Page ID: {page_id}")
    return database_id, page_id

def update_notion_task(database_id, page_id):
    try:
        # Query the Notion page
        page = notion.pages.retrieve(page_id=page_id)
        next_due = page['properties']['Next Due']['date']['start']
        logger.info(f"Next Due: {next_due}")

        # Update the page
        notion.pages.update(
            page_id=page_id,
            properties={ 
                'Due': {'date': {'start': next_due}},
                'Done': {'checkbox': False}
            }
        )
        logger.info("Page updated successfully.")
    except Exception as e:
        return generic_error_response(e)


def invalid_token_response():
    logger.error("Invalid Slack verification token.")
    return {
        'statusCode': 403,
        'body': json.dumps({'error': 'Invalid token'})
    }

def answer_challenge_response():
    challenge = body.get('challenge')
    return {
        'statusCode': 200,
        'body': json.dumps({'challenge': challenge})
    }

def unknown_event_response():
    logger.error(f"Unknown event type: {event_type}")
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Unknown event type'})
    }

def generic_error_response(e):
    logger.error(f"Error processing request: {e}")
    return {
        'statusCode': 500,
        'body': json.dumps({'error': 'Internal server error'})
    }