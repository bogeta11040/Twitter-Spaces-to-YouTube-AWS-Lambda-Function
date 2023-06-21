import tweepy
from tweepy import TweepyException
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests
import boto3

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

youtube_api_key = ''

twitter_usernames = ['BoraKonj', 'samodejo01', 'belcho1311', 'serbian_spaces', 'savamalac']

author_names = {
    'BoraKonj': 'Bora Konj',
    'samodejo01': 'Dejo',
    'belcho1311': 'Dragoslav Ljubicic',
    'serbian_spaces': 'Serbian Spaces',
    'savamalac': 'Jeremija'
}

# YouTube channel that we want spaces to be uploaded to
youtube_channel_id = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


youtube_service = build('youtube', 'v3', developerKey=youtube_api_key)


s3 = boto3.client('s3')


def download_twitter_space(space_id):
    # Download space and upload it to S3 bucket
    try:
        space = api.get_space(space_id)
        if space is not None and space.state == 'live' and space.is_recorded:
            video_url = space.recording.get('playbackUrl')
            response = requests.get(video_url, stream=True)
            if response.status_code == 200:
                video_file_path = f'videos/{space_id}.mp4'  # Putanja snimka u S3 bucket-u
                s3.upload_fileobj(response.raw, 'spejs', video_file_path)
                return True
    except tweepy.TweepyException as e:
        print(f'Error downloading Twitter Space: {e}')
    return False


def upload_to_youtube(video_file, video_title):
    try:
        youtube = youtube_service.videos()

        media = MediaFileUpload(video_file)

        request = youtube.insert(
            part='snippet,status',
            body={
                'snippet': {
                    'title': video_title,
                    'description': 'Ceo snimak spejsa. Snimci se postavljaju automatski.',
                },
                'status': {
                    'privacyStatus': 'public'
                }
            },
            media_body=media
        )

        response = request.execute()

        video_id = response['id']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        print(f'Successfully uploaded video to YouTube: {video_url}')
        delete_video_from_s3(video_file_path)
        return video_url
    except Exception as e:
        print(f'Error uploading video to YouTube: {e}')
    return None


def delete_video_from_s3(video_file_path):
    # Delete downloaded file from S3 bucket
    s3_client.delete_object(Bucket=bucket_name, Key=video_file_path)


def process_twitter_spaces(event, context):
    try:
        for username in twitter_usernames:
            user = api.get_user(screen_name=username)
            user_spaces = api.spaces(user_id=user.id, state='live')
            for space in user_spaces:
                space_id = space.id
                author_username = space.author.screen_name
                author_name = author_names.get(author_username, author_username)
                video_title = f"Spejs {author_name} {space.created_at.strftime('%d-%m-%Y')}"
                if download_twitter_space(space_id):
                    video_file_path = f's3://spejs/videos/{space_id}.mp4'
                    upload_to_youtube(video_file_path, video_title)
    except tweepy.TweepyException as e:
        print(f'Error fetching Twitter Spaces: {e}')


process_twitter_spaces(None, None)
