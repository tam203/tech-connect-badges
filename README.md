# Tech Connect Badges

A simple system for creating, granting and showing badges for Tech Connect members.

Badges are images in an S3 bucket with meta-data attached. The bucket is public read so available and awarded badges are public.

Awarded badges are stored with a key containing a users user id such as `/awarded/a4ad41/did_a_thing.png` where `did_a_thing.png` is the badge and `a4ad1` is the user id.

User ids are a hash of the users lowercased email address. Always use the same email for a user. If email address changes the users awarded badges will need to be renamed.

# Things in this repo.

# `tc_badges`

The python module for creating, awarding (and in future more) badges. Interface as a python module or using the script `badge.sh`

# `view.html`

An example html  page showing how to access a users badges and metadata given their id. open `view.html?user=<userid>` to test.

# Running the image badging up service

`FLASK_APP=tc_badges.badge_image flask run`

# Bucket set up.
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

# Using 

Ensure that you AWS credentials are set up, it's suggested you install the `aws-cli` and run `aws configure`. You must have permissions to write to the bucket being used. Run `scripts/badge.sh` to award, create, etc. 

## Requirements
* boto3
* Pillow
* Flask