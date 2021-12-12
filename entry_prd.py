import json
import boto3


def confirm_sign_up(email, confirmation_code):
    # 認証開始
    try:
        aws_client = boto3.client(
            'cognito-idp',
            region_name='ap-northeast-1',
            aws_access_key_id='',
            aws_secret_access_key='',
        )

        aws_result = aws_client.confirm_sign_up(
            ClientId="",
            Username=email,
            ConfirmationCode=confirmation_code,
        )

        # 本登録完了
        return aws_result

    except:
        # 認証失敗
        return 'error'


def handler(event, context):
    json_data = json.loads(event['body'])
    confirm_sign_up(json_data['email'], json_data['confirmation_code'])

    body = {
        "message": "prd successful",
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
