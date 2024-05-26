import boto3
import tweepy
import openpyxl
import random
import os

# Twitter APIの認証情報
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# S3 バケットとファイルの情報
s3_bucket = ''
excel_file_key = '.xlsx'

def download_file_from_s3():
    # S3 クライアントの作成
    s3 = boto3.client('s3')

    # ファイルをダウンロード
    local_file_path = '/tmp/file.xlsx'  # Lambda 内の一時ディレクトリに保存
    s3.download_file(s3_bucket, excel_file_key, local_file_path)

    return local_file_path

def get_random_tweet_content(file_path):
    # ExcelファイルからA列の値を取得
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # A列のデータが終了するまでのセルを取得
    a_column_values = [cell.value for cell in sheet['A'] if cell.value]

    workbook.close()

    if not a_column_values:
        # A列に値がない場合はエラーメッセージを返す
        return 'No values found in A column.'

    # ランダムに1つの値を選択
    random_tweet_content = random.choice(a_column_values)
    return random_tweet_content

def lambda_handler(event, context):
    # ファイルのダウンロード
    local_file_path = download_file_from_s3()

    # Twitter API認証
    #auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    #auth.set_access_token(access_token, access_token_secret)
    #api = tweepy.API(auth)

    # ツイート内容取得
    tweet_content = get_random_tweet_content(local_file_path)

    # A列に値がない場合はエラーを返す
    if 'No values found' in tweet_content:
        return {
            'statusCode': 500,
            'body': tweet_content
        }

    # ツイート投稿
    client = tweepy.Client(
        consumer_key        = consumer_key,
        consumer_secret     = consumer_secret,
        access_token        = access_token,
        access_token_secret = access_token_secret,
    )
    client.create_tweet(text = tweet_content)

    return {
        'statusCode': 200,
        'body': 'Random tweet posted successfully!'
    }