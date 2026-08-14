
class CartNotFoundError(Exception):
    pass


class CartItemNotFoundError(Exception):
    pass


class ProductOutOfStockError(Exception):
    pass


class InsufficientStockError(Exception):
    pass