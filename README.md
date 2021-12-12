# simple_authorization_project

## 構築手順

1. deploy対象のAWSアカウントをprofileファイルに記載
2. 定義したprofile名を用いて、コマンド実行 
   1. sls deploy --verbose --aws-profile <profile名>
3. deploy成功時、outputされる以下情報を控える。
   1. CognitoUserPoolIdARN 
   2. CognitoUserPoolClientId 
   3. CognitoUserPoolId
4. 各Lambdaの下記該当箇所にコピペしてください。
   1. entry_tmp.py
      1. line:10 aws_access_key_id=皆様の環境で利用できるアクセスキー
      2. line:11 aws_secret_access_key=皆様の環境で利用できるシークレットキー
      3. line:15 ClientId = CognitoUserPoolClientId
   2. entry_prd.py
      1. line:10 aws_access_key_id=皆様の環境で利用できるアクセスキー
      2. line:11 aws_secret_access_key=皆様の環境で利用できるシークレットキー
      3. line:15 ClientId = CognitoUserPoolClientId
   3. login.py
      1. line:10 aws_access_key_id=皆様の環境で利用できるアクセスキー
      2. line:11 aws_secret_access_key=皆様の環境で利用できるシークレットキー
      3. line:15 UserPoolId = CognitoUserPoolId
      4. line:16 ClientId = CognitoUserPoolClientId
5. 再度deployしてください。
   1. sls deploy --verbose --aws-profile <profile名>

これで構築完了です。


## 挙動確認手順

deploy成功結果に出力されているendpointsを利用します。

```
endpoints:
  GET - https://xxxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/hello
  POST - https://xxxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/entry/tmp
  POST - https://xxxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/entry/prd
  POST - https://xxxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/login
```

### メールアドレス、パスワードを利用して仮登録APIを叩く。  

```
curl -X POST -H "Content-Type: application/json" \
  -d '{"email":"xxxxxxxx@xxx.xxx", "password":"xxxxxxxxx"}' \
  https://xxxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/entry/tmp
...
{"message": "tmp successful"}
```

messageが **tmp successful** なら正常です。  
該当Cognitoを確認してみると、先ほど登録したメールアドレスに紐づいたユーザーがいるはずです。
仮登録に使用したメールアドレス宛に認証コードが届いていると思うので、コピペしておきましょう。

### 認証コードを利用して本登録APIを叩く。  

```
curl -X POST -H "Content-Type: application/json" \
  -d '{"email":"xxxxxxxx@xxx.xxx", "confirmation_code":"xxxxxx"}' \
  https://xxxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/entry/prd
...
{"message": "prd successful"}
```

messageが **prd successful** なら正常です。
該当Cognitoを確認してみると、先ほど登録したメールアドレスに紐づいたユーザーのステータスが変更されているはずです。
これでCognitoにユーザーとして認められた状態になりました。


### 登録で用いたメールアドレス、パスワードを利用して、ログインAPIを叩く。

```
curl -X POST -H "Content-Type: application/json" \
  -d '{"email":"xxxxxxxx@xxx.xxx", "password":"xxxxxxxxx"}' \
  https://xxxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/login
...
{"message": "login successful", "AccessToken": "eJraW...", "RefreshToken": "eyJjd....", "IdToken": "eyJra..."}
```

messageが **login successful** なら正常です。


### 返却された**Idtoken**をカスタムヘッダーに設定して、挨拶APIを叩く。  
messageが **Hello. CognitoUser!"** なら正常です。

```
curl https://xxxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/hello -H 'X-Auth:eyJra...'
...
{"message": "Hello. CognitoUser!"}
```
