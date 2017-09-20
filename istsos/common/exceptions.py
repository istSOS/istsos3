# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0


class SosException(Exception):

    def __init__(self, message=None, status_code=-1):
        super(SosException, self).__init__(message)
        self.message = message
        self.status_code = status_code

    def to_xml(self):
        return (
            "<Exception exceptionCode=\"InvalidParameterValue\""
            "locator=\"version\"/>"
        )


class InvalidParameterValue(SosException):

    message = (
        "Operation request contains an invalid parameter"
        "InvalidParameterValue value"
    )

    def __init__(self, locator, message=None):
        super(InvalidParameterValue, self).__init__(
            message if message is not None else self.message,
            "InvalidParameterValue"
        )
        self.locator = locator

    def to_xml(self):
        return (
            """<Exception
        exceptionCode=\"InvalidParameterValue\"
        locator=\"%s\">
        <ExceptionText>%s</ExceptionText>
    </Exception>""" % (self.locator, self.message)
        )


class DbError(SosException):
    """
    """
    def __init__(self, message=None, status_code=-1):
        super(DbError, self).__init__(message)
        self.message = message
        self.status_code = status_code
