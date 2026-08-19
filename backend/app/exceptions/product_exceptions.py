
class ProductNotFoundError(Exception):
    pass


class ProductAlreadyExistsError(Exception):
    pass


class MinPriceGreaterThanMaxPriceError(Exception):
    pass
