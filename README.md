# Tech Connect Badges

A simple system for creating, granting and showing badges for Tech Connect members.

Badges that can be awarded are images in an S3 bucket with meta-data attached. Awards, are JSON docs detailing the award. The bucket is public read so available and awarded badges are public.

Awarded badges are stored with a key containing a users user id such as `/awarded/a4ad41/did_a_thing.png` where `did_a_thing.png` is the badge and `a4ad1` is the user id.

User ids are a hash of the users lower cased email address. Always use the same email for a user. If email address changes the users awarded badges will need to be renamed.

## Things in this repo.

### `tc_badges`

The python module for creating, awarding (and in future more) badges. Interface as a python module or using the script `badge.sh`

Use python 3.6 and a virtual env.

Set up:
```
python -m venv tc-badges-env
source tc-badges-env/bin/activate
pip install -r requirements.txt
```

If you have problems installing pillow try `brew install libjpeg zlib` (if on mac) and try `pip install -r requirements.txt` again (from https://stackoverflow.com/a/34631976/1498817).

[*] Depending on your set up you might need to use `pip3`.

Once set up next time just use  `source ./tc-badges-env/bin/activate`

Note zappa doesn't work with conda. I brew installed python and ensured I was using that version to create the venv

### `view.html`

An example html page showing how to access a users badges and metadata given their id. open `view.html?user=<userid>` to test.


## Bucket set up.
The bucket permissions (ACL) are set to *Everyone: List objects*. Badges are uploaded with public read permissions (when using the python module). 

CORS is set up as below:

```
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>HEAD</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <ExposeHeader>x-amz-meta-name</ExposeHeader>
    <ExposeHeader>x-amz-meta-rank</ExposeHeader>
    <ExposeHeader>x-amz-meta-reason-awarded</ExposeHeader>
    <ExposeHeader>x-amz-meta-date</ExposeHeader>
    <ExposeHeader>x-amz-meta-awarded-for</ExposeHeader>
    <AllowedHeader>Authorization</AllowedHeader>
    <AllowedHeader>x-amz-meta-name</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```

## Using 
Ensure the environment variable `TC_BADGES_BUCKET` is set. Production is `tech-connect-badges`, dev `tech-connect-badges-dev`
Ensure that you AWS credentials are set up, it's suggested you install the `aws-cli` and run `aws configure`. You must have permissions to write to the bucket being used. Run `scripts/badge.sh` to award, create, etc. 

## Yammer app

### Deploy

`zappa deploy dev` or `zappa update dev`

This will deploy the app and give you a url, this will be your redirect url.  After the deploy and after registering your app you'll need to update the lambda with `CLIENT_ID` and `CLIENT_SECRET` variables. These can be got in the next step.


### Yammer app

You will also need to register the app at https://www.yammer.com/client_applications see https://developer.yammer.com/docs for more info. 
You will need the deployed url that `zappa` returns as your "callback" or "welcome" url. 
Registering will give you a `client_id` and `client_secret`.

This link is where you can manage your apps once registered https://www.yammer.com/client_applications 

This is a template for the link users will need to click to use the app `https://www.yammer.com/oauth2/authorize?client_id=<client_id>&response_type=code&redirect_uri=<deployment_uri>`

fore example 

`https://www.yammer.com/oauth2/authorize?client_id=vsqHmLkUHYwEjW4sgJHwLQ&response_type=code&redirect_uri=https://484f162c.ngrok.io?action=get-most-like-yammer&new_than=1109052882`


### Running the image badging up service

`CLIENT_ID=<client_id> CLIENT_SECRET=<client_secret> FLASK_APP=tc_badges.server.apps flask run`



## Requirements
See `requirements.txt`, but:
* boto3
* Pillow
* Flask
* zappa

## Running test
TC_BADGES_BUCKET=None python -m unittest discover tests