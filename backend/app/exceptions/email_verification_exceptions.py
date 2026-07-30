class InvalidVerificationTokenError(Exception):
    pass


class VerificationTokenExpiredError(Exception):
    pass


class EmailAlreadyVerifiedError(Exception):
    pass