import boto3
from datetime import date, timedelta

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

applies_table = dynamodb.Table('applies')
user_table = dynamodb.Table('users')

def email_alarm(event, context):
    today = date.today()
    target_date = today + timedelta(days=1)

    response = applies_table.scan()
    for item in response.get('Items', []):
        deadline = item.get('deadline_date')
        document = item.get("document_result_date")
        interview = item.get("interview_date")
        final = item.get("final_date")
        user_pk=item.get('PK')
        post_name=item.get('post_name')
        if deadline:
            month, day = map(int, deadline.split('(')[0].split('.'))
            deadline = date(today.year, month, day)
            if deadline == target_date:
                print(f"{user_pk}, {deadline}")
                send_email(user_pk, "Deadline Date", post_name)
        if document:
            document = date.fromisoformat(document.split("T")[0])
            if document == target_date:
                print(f"{user_pk}, {document}")
                send_email(user_pk, "Document Result Date", post_name)
        if interview:
            interview = date.fromisoformat(interview.split("T")[0])
            if interview == target_date:
                print(f"{user_pk}, {interview}")
                send_email(user_pk, "Interview Date", post_name)
        if final:
            final = date.fromisoformat(final.split("T")[0])
            if final == target_date:
                print(f"{user_pk}, {final}")
                send_email(user_pk, "Final Date", post_name)
            

def send_email(user_pk, type, title):
    user_response = user_table.get_item(Key={'PK': user_pk})
    user = user_response.get('Item')
    email = user.get('user_email')
    if email:
        print(f"Send Email: {email}")
        ses.send_email(
            Source="piwhyjey@gmail.com",
            Destination={
                'ToAddresses': [email]
            },
            Message={
                'Subject': {
                    'Data': f"Your Applies {type} Reminder : {title}"
                },
                'Body': {
                    'Text': {
                        'Data': f"Your Applies Post: {title}\nYour Applies {type} is tomorrow!"
                    }
                }
            }
        )