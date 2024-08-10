from .print_stylized_tables import sp_users, sp_cars, sp_brands_models, sp_orders


def print_users(order_by="Id", desc_order=False):
    sp_users(order_by, desc_order)


def print_cars(order_by="Id", desc_order=False):
    sp_cars(order_by, desc_order)


def print_brands_models(order_by="Id", desc_order=False):
    sp_brands_models(order_by, desc_order)


def print_orders(order_by="Id", desc_order=False):
    sp_orders(order_by, desc_order)


if __name__ == "__main__":
    sp_orders()
