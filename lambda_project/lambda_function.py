import json
import os
import logging
import re
from notion_client import Client
import requests

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment variables
NOTION_API_TOKEN = os.getenv('NOTION_API_TOKEN')
SLACK_VERIFICATION_TOKEN = os.getenv('SLACK_VERIFICATION_TOKEN')



def lambda_handler(event, context):
    try:
        body = event.get('body', event)
        if type(body) is str:
            body = json.loads(body)
            
        slack_token = body.get('token')
        event_type = body.get('type')
        # logger.info(f"Received Slack body: {body}")

        if slack_token != SLACK_VERIFICATION_TOKEN:
            return invalid_token_response()

        if event_type == 'url_verification':
            return answer_challenge_response(body)
        elif event_type == 'event_callback':
            return handle_event_callback(body)
        else:
            return unknown_event_response(event_type)

    except Exception as e:
        return generic_error_response(e)


def handle_event_callback(body):
    database_id, page_id = parse_event_text(body)
    update_notion_task(database_id, page_id)

    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'success'})
    }

def parse_event_text(body):
    event_data = body.get('event', {})
    blocks = event_data.get('blocks', [])
    
    elements = [e.get('text') for b in blocks for e in b.get('elements', []) if type(e.get('text', None)) is str]
    fields = [e.get('text') for b in blocks for e in b.get('fields', []) if type(e.get('text', None)) is str]
    message_text = event_data.get('text', '') + '\n'.join(elements) + '\n'.join(fields)
    # logger.info(f"Received Slack event: {message_text}")

    # Extract Notion Database ID and Page ID from the message
    matches = re.findall(r"\.so\/([a-z0-9]{32})\?.*\s.*([a-z0-9]{32})\?", message_text)[0]
    logger.info(f"Database ID: {matches[0]}, Page ID: {matches[1]}")
    
    return matches[0], matches[1]

def update_notion_task(database_id, page_id):
    notion = Client(auth=NOTION_API_TOKEN)
    try:
        # Query the Notion page
        page = notion.pages.retrieve(page_id=page_id)
        # logger.info(f"Page:\n{page}")
        if not page['properties'].get('Task', False): 
            return
        
        due = page['properties']['Due']
        next_due = page['properties']['Next Due']['formula']
        title = page['properties']['Task']['title'][0]['plain_text']
        done = page['properties']['Done']['checkbox']
        
        if next_due['type'] != 'date' or not done:
            return

        # Update the page
        logger.warn(f'Updating page {title} due from {due} to {next_due}, was done {done}')
        notion.pages.update(
            page_id=page_id,
            properties={ 
                'Due': next_due,
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

def answer_challenge_response(body):
    challenge = body.get('challenge')
    return {
        'statusCode': 200,
        'body': json.dumps({'challenge': challenge})
    }

def unknown_event_response(event_type):
    logger.error(f"Unknown event type: {event_type}")
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Unknown event type'})
    }

def generic_error_response(e):
    logger.exception(f"Error processing request: {e}")
    return {
        'statusCode': 500,
        'body': json.dumps({'error': 'Internal server error'})
    }
