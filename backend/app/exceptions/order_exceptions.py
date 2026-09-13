# Raised when an order status transition is not allowed.
class InvalidOrderStatusTransitionError(Exception):
    pass

# Raised when an order cannot be found.
class OrderNotFoundError(Exception):
    pass