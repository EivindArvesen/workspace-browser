#!/usr/bin/env bash

sphinx-apidoc -F -o docs raskolnikov


# def _validate(cls, method, resource=None):
# """Return ``True`` if the the given *cls* supports the HTTP *method* found
# on the incoming HTTP request.
#
# :param cls: class associated with the request's endpoint
# :type cls: :class:`sandman.model.Model` instance
# :param string method: HTTP method of incoming request
# :param resource: *cls* instance associated with the request
# :type resource: :class:`sandman.model.Model` or None
# :rtype: bool
#
# """
# if not method in cls.__methods__:
#     return False
#
# class_validator_name = 'validate_' + method
#
# if hasattr(cls, class_validator_name):
#     class_validator = getattr(cls, class_validator_name)
#     return class_validator(resource)
#
# return True
# """
