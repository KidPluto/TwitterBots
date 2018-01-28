import boto3
from botocore.exceptions import ClientError

from twython import Twython, TwythonError

# Twitter creds
APP_KEY='12345'
APP_SECRET='12345'
OAUTH_TOKEN='12345'
OAUTH_TOKEN_SECRET='12345'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
try:
    search_results = twitter.search(q='#HashtagToSearchFor', count=5)
except TwythonError as e:
    print e

filename = "tweets-ouput.txt"
file = open(filename,"w")

for tweet in search_results['statuses']:
    file.write('Tweet from @%s Date: %s' % (tweet['user']['screen_name'].encode('utf-8'),tweet['created_at']))
    file.write('\n')
    file.write(tweet['text'].encode('utf-8'))
    file.write('\n\n')
file.close()

SENDER = "Twitter bot <your@email.address>"
RECIPIENT = "recipient@email.address"
AWS_REGION = "us-east-1"
SUBJECT = "Latest 5 tweets for Hashtag ..."

file = open(filename,"r")
BODY_TEXT = file.read()
file.close()

CHARSET = "UTF-8"

client = boto3.client('ses',region_name=AWS_REGION)

# Try to send the email.
try:
    #Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER
    )
# Display an error if something goes wrong.
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['ResponseMetadata']['RequestId'])
