from flask import request, jsonify
from app import logger
from app.prices import bp
from app.models import Prices
from app.schemas import PriceRequestDeserializingSchema
from app.errors.handlers import bad_request, not_found

from flask_jwt_extended import jwt_required

from marshmallow import ValidationError

# Declare schema for parsing request
price_request_schema = PriceRequestDeserializingSchema()


@bp.get("/tariff")
@jwt_required()
def get_tariff() -> str:
    """
    Lets users find the tariff

    Returns
    -------
    str
        A JSON object containing the tariff price
    """
    try:
        result = price_request_schema.load(request.json)
    except ValidationError as e:
        return bad_request(e.messages)

    # Fetch prices for the request data from database
    prices = (
        Prices.query.filter(Prices.postal_code == result["zip_code"])
        .filter(Prices.city == result["city"])
        .filter(Prices.street == result["street"])
        .filter(Prices.house_no_max >= result["house_number"])
        .filter(Prices.house_no_min <= result["house_number"])
        .all()
    )

    # If no prices found return 404
    if len(prices) == 0:
        return not_found("Tariff not found")

    # calculate the total tariff
    total_tariff = calculate_total_tariff(prices, result["yearly_kwh_consumption"])

    return jsonify(total_tariff), 200


def calculate_total_tariff(prices, consumption):
    """
    Calculate total tariff for given prices and consumption
    Parameters
    ----------
    prices - List of Prices objects
    consumption - consumption

    Returns
    -------
    Return total tariff object

    """
    price_list = []
    for price in prices:
        price_list.append(calculate_tariff(price, consumption))
    avg_price = {}
    for key in price_list[0].keys():
        avg_price[key] = round(sum(d[key] for d in price_list) / len(price_list), 2)
    return avg_price


def calculate_tariff(price, consumption):
    """

    Parameters
    ----------
    price - Single price object
    consumption - consumption

    Returns
    -------
    tariff object for the price

    """
    return {
        "unit_price": price.unit_price,
        "grid_fees": price.grid_fee,
        "kwh_price": price.kwh_price,
        "total_price": price.unit_price
        + price.grid_fee
        + round(price.kwh_price * consumption, 2),
    }
