"""
This Module contains an AuthenticationManager that can authenticate and identify users with jwt tokens using
IdentityProviders
"""
import gettext
import os
import sys

from learnlytics.authentication.providers.identity_provider import IdentityProvider
from .authentication_manager import AuthenticationManager, auth_required
from .util import current_identity

__all__ = ["AuthenticationManager", "auth_required", "current_identity"]
