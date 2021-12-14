import json
import boto3


def sign_up(email, password):
    # 認証開始
    try:
        aws_client = boto3.client(
            'cognito-idp',
            region_name='ap-northeast-1',
            aws_access_key_id='',
            aws_secret_access_key='',
        )

        aws_result = aws_client.sign_up(
            ClientId="",
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ]
        )

        # 仮登録完了
        return aws_result

    except:
        # 認証失敗
        return 'error'


def handler(event, context):
    json_data = json.loads(event['body'])
    sign_up(json_data['email'], json_data['password'])

    body = {
        "message": "tmp successful",
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
