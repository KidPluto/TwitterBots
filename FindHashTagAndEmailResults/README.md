The idea
=====
* Receive an email each morning, which would show me the lastest tweets for a given hashtag.
* Use Python, so I can put that on my resume.  (Someone please explain to me why Perl is not bing used anymore.)
* Write the least possible amount of Python, do not reinvent the wheel.
  * Use Twython to access Twitter.
  * Use AWS to host and run the script.
  * Use AWS Simple Email Service to send the email.

Needed for any Twitter bot
=====
* Create Twitter account
  * Create Twitter App - this gives you the Twitter crendials you need
* Create AWS account
  * Create AWS EC2 instance
    * Select Amazon Linux, and take all the default selections.  This comes with python v2
  * Install [Twython](https://twython.readthedocs.io/en/latest/)
    * `sudo pip install twython`

Specific to this twitter bot
=====
* Set up AWS SES (Simple Email Service), good guide [here](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html)  The steps I used:
  * Verify your email address with Amazon SES
  * Install the AWS SDK for Python (Boto)
* Create `config.txt`
  * Your file would just contain the values in the Example column.  The values in the Example column below are examples only.

Value|Example
-----|-------
Twitter app key|lajd;jasdlfkj
Twitter app secret|l;akjdjf;ajdf;
Twitter oauth token|alsjdflajdl
Twitter oauth token secret|lakdfjlajsdfk
Hashtag to search for|#Boston
Senders email address|you@email.com
Receipents email address|you@email.com
Number of tweets to search for|50

* Move this script, and the configurations file to your EC2 instance.  Place in "python-scripts" subdirectory.

* Create crontab, to run the script once a day:

`00 06 * * * python /home/ec2-user/python-scripts/FindHashTagAndEmailResults.py`



