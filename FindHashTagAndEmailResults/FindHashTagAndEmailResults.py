#
import boto3
from botocore.exceptions import ClientError
from twython import Twython, TwythonError

# Read in all values from config file
file = open("/home/ec2-user/python-scripts/config.txt","r")
APP_KEY                     = file.readline().strip()
APP_SECRET                  = file.readline().strip()
OAUTH_TOKEN                 = file.readline().strip()
OAUTH_TOKEN_SECRET          = file.readline().strip()
#
HASHTAG_TO_SEARCH_FOR       = file.readline().strip()
FROM_EMAIL                  = file.readline().strip()
TO_EMAIL                    = file.readline().strip()
NUMBER_OF_TWEETS_TO_RETURN  = file.readline().strip()
file.close()

# Call Twitter API
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
try:
    search_results = twitter.search(q=HASHTAG_TO_SEARCH_FOR, count=NUMBER_OF_TWEETS_TO_RETURN, result_type='recent')
except TwythonError as e:
    print(e.response['Error']['Message'])

# Write results out to temp file
filename = "tweets-output.txt"
file = open(filename,"w")
for tweet in search_results['statuses']:
    file.write('Tweet from @%s' % (tweet['user']['screen_name'].encode('utf-8')))
    file.write('\n')
    file.write(tweet['text'].encode('utf-8'))
    file.write('\n\n')
file.close()

# Set up variables to be used by call to SDS
CHARSET = "UTF-8"
AWS_REGION = "us-east-1"
SUBJECT = "This is your Twitter bot ..."
# Contents of temp file, to the body of the email
file = open(filename,"r")
BODY_TEXT = file.read()
file.close()

# Call AWS SDS API
client = boto3.client('ses',region_name=AWS_REGION)
try:
    #Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [
                TO_EMAIL,
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
        Source=FROM_EMAIL
    )
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['ResponseMetadata']['RequestId'])
