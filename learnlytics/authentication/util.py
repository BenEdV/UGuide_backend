"""
This Module contains some helpful functions not linked to objects
"""

from flask_jwt_extended import current_user

from learnlytics.authentication.providers import PlainTextProvider, LdapProvider, LocalProvider, SAMLProvider


def current_identity():
    """
    Flask-JWT wraps  the User object in a LocalProxy, thus it's not
    of type 'User' and we can't simply marshal it. Hence we call
    _get_current_object to unwrap the LocalProxy and retrieve the User
    so that we can serialise to JSON

    See: http://werkzeug.pocoo.org/docs/0.11/local/
    """
    # pylint: disable=protected-access
    return current_user


def _initialise_providers(app, load_user_func, add_user_func):
    """
    Function loads IdentityProvider objects from the config settings of the application object
    :param app: Flask application object with the config containing the settings under the "IDENTITY_PROVIDERS" key
    :param load_user_func: function that loads the user based on name and IdentityProvider name
    :param add_user_func: function that adds the user based on name and IdentityProvider name and info in kwargs
     arguments
    :return: list of IdentityProvider objects loaded form config
    """
    provider_conf = app.config.get("IDENTITY_PROVIDERS", None)
    if provider_conf is None:
        return dict()

    _identity_providers = {}
    if provider_conf:
        if provider_conf.get('Test', None):
            for name, conf in provider_conf['Test'].items():
                _identity_providers[name] = PlainTextProvider(name, load_user_func, add_user_func, conf)

        if provider_conf.get('Local', None):
            for name, conf in provider_conf['Local'].items():
                _identity_providers[name] = LocalProvider(name, load_user_func, conf)

        if provider_conf.get('LDAP', None):
            for name, conf in provider_conf['LDAP'].items():
                _identity_providers[name] = LdapProvider(name, load_user_func, add_user_func, conf)

        if provider_conf.get('SAML', None):
            for name, conf in provider_conf['SAML'].items():
                _identity_providers[name] = SAMLProvider(name, load_user_func, add_user_func, conf)

    return _identity_providers
