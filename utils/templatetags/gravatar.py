import hashlib
import urllib
from django_jinja import library, utils


@library.global_function
def gravatar_url(email=None, size=40):
    """
    return only the URL of the gravatar
    TEMPLATE USE:  {{ gravatar_url(email, 150) }}
    """
    # TODO: change default image
    default = "https://www.ucas.com/sites/default/files/default_images/default_avatar.png"
    email = email.encode("utf-8")
    md5_hash = hashlib.md5(email.lower()).hexdigest()
    params = urllib.parse.urlencode({"d": default, "s": str(size)})
    return f"https://www.gravatar.com/avatar/{md5_hash}?{params}"


@library.global_function
@utils.safe
def gravatar(email, size=40):
    """
    return an image tag with the gravatar
    TEMPLATE USE:  {{ gravatar(email, 150) }}
    """
    url = gravatar_url(email, size)
    return f'<img src="{url}" height="{size}" width="{size}">'
