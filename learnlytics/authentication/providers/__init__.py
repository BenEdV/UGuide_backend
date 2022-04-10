"""
This module contains several identityprovider implementations
"""
from .ldap_provider import LdapProvider
from .plaintext_provider import PlainTextProvider
from .local_provider import LocalProvider
from .saml_provider import SAMLProvider
