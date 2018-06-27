from hashlib import sha256
import re


def get_id(email):
    email = email.lower().strip()
    return sha256(email.encode('utf-8')).hexdigest()[:6]


def slug(name):
    slug = re.sub('[ -]+', '_', name)
    slug = re.sub('\W', '', slug).lower().strip()
    return slug
