import unittest
from app import create_app, db
from app.helpers.test_helpers import register_and_login_test_user
from app.models import Prices
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SECRET_KEY = "SQL-SECRET"
    JWT_SECRET_KEY = "JWT-SECRET"


class TestPrices(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_tariff(self):
        with self.app.test_client() as c:
            setup_access_token = register_and_login_test_user(c)

            payload = {
                "zip_code": 10555,
                "city": "Nellischeid",
                "street": "Torstraße",
                "house_number": 26,
                "yearly_kwh_consumption": 1000
            }

            price = Prices(**{
                "postal_code": 10555,
                "city": 'Nellischeid',
                "street": 'Torstraße',
                "house_no_min": 20,
                "house_no_max": 30,
                "unit_price": 1.66,
                "grid_fee": 3.99,
                "kwh_price": 0.58,
            })

            db.session.add(price)
            db.session.commit()

            resp = c.post(
                "/api/price/tariff",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
                json=payload,
            )

            json_data = resp.get_json()
            self.assertEqual(585.65, json_data['total_price'])
            self.assertEqual(200, resp.status_code, msg=json_data)

    def test_get_tariff_with_multiple_prices(self):
        with self.app.test_client() as c:
            setup_access_token = register_and_login_test_user(c)

            payload = {
                "zip_code": 10555,
                "city": "Nellischeid",
                "street": "Torstraße",
                "house_number": 26,
                "yearly_kwh_consumption": 1000
            }

            price1 = Prices(**{
                "postal_code": 10555,
                "city": 'Nellischeid',
                "street": 'Torstraße',
                "house_no_min": 20,
                "house_no_max": 30,
                "unit_price": 1.66,
                "grid_fee": 3.99,
                "kwh_price": 0.58,
            })

            price2 = Prices(**{
                "postal_code": 10555,
                "city": 'Nellischeid',
                "street": 'Torstraße',
                "house_no_min": 20,
                "house_no_max": 30,
                "unit_price": 1.50,
                "grid_fee": 3.20,
                "kwh_price": 0.40,
            })

            db.session.add(price1)
            db.session.add(price2)
            db.session.commit()

            resp = c.post(
                "/api/price/tariff",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
                json=payload,
            )

            json_data = resp.get_json()
            self.assertEqual(495.17, json_data['total_price'])
            self.assertEqual(200, resp.status_code, msg=json_data)


    def test_get_tariff_when_price_not_found(self):
        with self.app.test_client() as c:
            setup_access_token = register_and_login_test_user(c)

            payload = {
                "zip_code": 10555,
                "city": "Nellischeid",
                "street": "Torstraße",
                "house_number": 26,
                "yearly_kwh_consumption": 1000
            }

            price = Prices(**{
                "postal_code": 10555,
                "city": 'Nellischeid',
                "street": 'Torstraße',
                "house_no_min": 20,
                "house_no_max": 25,
                "unit_price": 1.66,
                "grid_fee": 3.99,
                "kwh_price": 0.58,
            })

            db.session.add(price)
            db.session.commit()

            resp = c.post(
                "/api/price/tariff",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
                json=payload,
            )

            json_data = resp.get_json()
            self.assertEqual(404, resp.status_code, msg=json_data)


    def test_get_tariff_for_invalid_request(self):
        with self.app.test_client() as c:
            setup_access_token = register_and_login_test_user(c)

            payload = {
                "zip_code": 10555,
                "city": "Nellischeid",
                "street": "Torstraße",
                "house_number": 26,
                "yearly_kwh_consumption": ""
            }

            price = Prices(**{
                "postal_code": 10555,
                "city": 'Nellischeid',
                "street": 'Torstraße',
                "house_no_min": 20,
                "house_no_max": 25,
                "unit_price": 1.66,
                "grid_fee": 3.99,
                "kwh_price": 0.58,
            })

            db.session.add(price)
            db.session.commit()

            resp = c.post(
                "/api/price/tariff",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
                json=payload,
            )

            json_data = resp.get_json()
            self.assertEqual(400, resp.status_code, msg=json_data)

if __name__ == "__main__":
    unittest.main()
