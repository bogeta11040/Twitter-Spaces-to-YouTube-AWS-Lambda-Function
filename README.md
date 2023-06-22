# Twitter Spaces to YouTube Lambda Function

This AWS Lambda function allows you to automatically download Twitter Spaces recordings and upload them to a YouTube channel.

## Prerequisites

- AWS account
- (Basic or Pro) Twitter Developer account with API keys
- Google Developer account with YouTube API key

## Setup

1. Create an AWS Lambda function using this code. Make sure to set the necessary environment variables for your Twitter and YouTube API credentials.

2. Change the handler function name in the Lambda function configuration to `process_twitter_spaces`.

3. Configure the required AWS permissions for the Lambda function to access S3, CloudWatch, etc.

4. Set up an S3 bucket to store the downloaded Twitter Spaces recordings. Name your bucket `spejs`.

5. Configure the necessary API credentials and permissions on the Twitter Developer portal and Google Developer console.

6. Create a YouTube channel and obtain the channel ID.

7. Update the configuration variables in the code, such as `consumer_key`, `consumer_secret`, `access_token`, `access_token_secret`, `youtube_api_key`, `twitter_usernames`, and `youtube_channel_id` with your own values.

8. Open your IDE, copy the code and run the following command to install the required packages:

```
pip install tweepy google-api-python-client requests boto3
```

9. Zip the files and upload the resulting archive as code to the AWS Lambda service.

10. Deploy the Lambda function and test it by triggering it manually or setting up a schedule using CloudWatch Events.

## Functionality

1. The function fetches live Twitter Spaces from the specified Twitter usernames.

2. If a live Twitter Space is recorded, it downloads the recording and uploads it to the specified S3 bucket.

3. It then uploads the video to the specified YouTube channel using the YouTube API.

4. Once the video has been uploaded, it is subsequently removed from the S3 bucket.

5. The function logs the success or failure of each operation.
