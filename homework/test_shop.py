"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100.10, "This is a book", 1000)


@pytest.fixture
def product2():
    return Product("water", 50.05, "This is a bottle of water", 20000)


@pytest.fixture
def empty_cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    # tests for checking quantity

    def test_product_check_quantity_positive(self, product):
        assert product.check_quantity(999) is True

    def test_product_check_exact_quantity_positive(self, product):
        assert product.check_quantity(1000) is True

    def test_product_check_quantity_negative(self, product):
        assert product.check_quantity(1001) is False

    # ============================
    # tests for decreasing product while buying

    def test_product_buy_positive(self, product, quantity_to_buy=999):
        expected_quantity = product.quantity - quantity_to_buy
        product.buy(quantity_to_buy)
        assert expected_quantity == product.quantity

    def test_product2_buy_positive(self, product2, quantity_to_buy=1000):
        expected_quantity = product2.quantity - quantity_to_buy
        product2.buy(quantity_to_buy)
        assert expected_quantity == product2.quantity

    def test_product_buy_more_than_available(self, product, quantity_to_buy=1001):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError) as error:
            product.buy(quantity_to_buy)
        assert str(error.value) == f"Не хватает продукта {product.name}."

    # ============================


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    # tests for adding products

    def test_add_product_to_empty_cart(self, empty_cart, product, buy_count=999):
        empty_cart.add_product(product, buy_count)
        assert empty_cart.products[product] == buy_count

    def test_add_several_products_to_empty_cart(self, empty_cart, product, buy_count=999):
        empty_cart.add_product(product, buy_count)
        empty_cart.add_product(product, 1)
        assert empty_cart.products[product] == buy_count + 1

    def test_add(self, empty_cart, product, buy_count=1001):
        with pytest.raises(ValueError) as error:
            empty_cart.add_product(product, buy_count)
        assert str(error.value) == f"Вы пытаетесь добавить в корзину {product.name}, но его нет в таком количестве"

    # ============================
    # tests for removing products

    def test_remove_product(self, empty_cart, product, buy_count=1000, remove_count=1):
        expected_count = buy_count - remove_count
        empty_cart.add_product(product, buy_count)
        empty_cart.remove_product(product, remove_count)
        assert empty_cart.products[product] == expected_count

    def test_remove_every_item_of_product(self, empty_cart, product, buy_count=999, remove_count=999):
        empty_cart.add_product(product, buy_count)
        empty_cart.remove_product(product, remove_count)
        assert empty_cart.products == {}

    def test_fast_remove_every_item_of_product(self, empty_cart, product, buy_count=1000):
        empty_cart.add_product(product, buy_count)
        empty_cart.remove_product(product)
        assert empty_cart.products == {}

    def test_remove_absent_in_cart_product(self, empty_cart, product, product2, buy_count=555):
        empty_cart.add_product(product2, buy_count)
        with pytest.raises(ValueError) as error:
            empty_cart.remove_product(product)
        assert str(error.value) == f"Продукта {product.name} нет в корзине."

    # ============================
    # tests for clearing cart

    def test_clear_cart(self, empty_cart, product, product2, buy_count=500):
        empty_cart.add_product(product, buy_count)
        empty_cart.add_product(product2, buy_count)
        empty_cart.clear()
        assert empty_cart.products == {}

    def test_clear_empty_cart(self, empty_cart):
        empty_cart.clear()
        assert empty_cart.products == {}

    # ============================
    # tests for getting total price

    def test_get_total_price_for_empty_cart(self, empty_cart):
        assert empty_cart.get_total_price() == 0

    @pytest.mark.parametrize("product_amount, product2_amount, expected_total_price", [
        (1, 1, 150.15),
        (0, 1, 50.05),
        (0, 100, 5005),
        (1, 0, 100.1),
        (10, 0, 1001),
        (1000, 20000, 1101100),
        (555, 10, 56056),
    ])
    def test_get_total_price_for_filled_cart(self, empty_cart, product, product2,
                                             product_amount, product2_amount, expected_total_price):
        empty_cart.add_product(product, product_amount)
        empty_cart.add_product(product2, product2_amount)
        assert empty_cart.get_total_price() == pytest.approx(expected_total_price)

    # ============================
    # tests for buying products

    """
    # На данный момент не достижимый тест, так как при добавлении продуктов больше, чем есть высветится другое
    # предупреждение. Но может потребоваться в будущем, если добавятся какие-то новые методы в обход существующим
    
        def test_buy_products_from_cart_more_than_available(self, empty_cart, product, buy_count=50000):
        empty_cart.add_product(product, buy_count)
        with pytest.raises(ValueError) as error:
            empty_cart.buy()
        assert str(error.value) == f"Товара {product.name} не хватает на складе"
    """

    @pytest.mark.parametrize("product_amount, product2_amount, expected_product_quantity, expected_product2_quantity", [
        (1, 1, 999, 19999),
        (0, 1, 1000, 19999),
        (1, 0, 999, 20000),
        (1000, 20000, 0, 0),
        (400, 5000, 600, 15000),
    ])
    def test_buy_products_from_cart(self, empty_cart, product, product2,
                                    product_amount, product2_amount,
                                    expected_product_quantity, expected_product2_quantity):
        empty_cart.add_product(product, product_amount)
        empty_cart.add_product(product2, product2_amount)
        empty_cart.buy()
        assert (product.quantity == expected_product_quantity
                and product2.quantity == expected_product2_quantity
                and empty_cart.products == {})

    # ============================
