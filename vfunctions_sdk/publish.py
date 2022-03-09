#!/usr/bin/env python3

import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

SENDER = "vfunction@verifiably.com"
AWS_REGION = "us-east-2"
SUBJECT = "Response from enclave"
CHARSET = "utf-8"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = "Hello,\r\nPlease see the attached attestation doc with the result of your vFunction."

# The HTML body of the email.
BODY_HTML = """\
<html>
<head></head>
<body>
<p>Hello!</p>
<p>Please see the attached attestation doc with the result of your vFunction.</p>
</body>
</html>
"""

def send_email(recipient, att_doc, aws_credentials):
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',
        region_name = aws_credentials["Region"],
        aws_access_key_id = aws_credentials["AccessKeyId"],
        aws_secret_access_key = aws_credentials["SecretAccessKey"],
        aws_session_token = aws_credentials["SessionToken"])


    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = recipient

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    # Define the attachment part and encode it using MIMEApplication.
    att = MIMEApplication(att_doc)
    att.add_header('Content-Disposition','attachment',filename=os.path.basename("result_att_doc.txt"))
    msg.attach(msg_body)

    # Add the attachment to the parent container.
    msg.attach(att)

    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[
                recipient
            ],
            RawMessage={
                'Data':msg.as_string(),
            },
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
