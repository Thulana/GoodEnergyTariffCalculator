from flask import request, jsonify

from app import db
from app.prices import bp
from app.models import Prices
from app.schemas import PricesSchema, PriceRequestDeserializingSchema
from app.errors.handlers import bad_request, not_found

from flask_jwt_extended import jwt_required, current_user

from marshmallow import ValidationError

import asyncio
from aiohttp import ClientSession

# Declare database schemas so they can be returned as JSON objects
price_request_schema = PriceRequestDeserializingSchema()


@bp.post("/tariff")
@jwt_required()
def get_tariff() -> str:
    """
    Lets users find the tariff

    Returns
    -------
    str
        A JSON object containing a success message
    """
    try:
        result = price_request_schema.load(request.json)
    except ValidationError as e:
        return bad_request(e.messages)

    prices = Prices.query.filter(Prices.postal_code == result['zip_code']).filter(Prices.city == result['city'])\
        .filter(Prices.street == result['street']).filter(Prices.house_no_max >= result['house_number']).filter(Prices.house_no_min <= result['house_number']).all()

    print(prices)
    if len(prices) == 0:
        return not_found("Tariff not found")

    total_tariff = calculate_total_tariff(prices,result['yearly_kwh_consumption'])

    return jsonify(total_tariff), 200


def calculate_total_tariff(prices, consumption):
    price_list = []
    for price in prices:
        price_list.append(calculate_tariff(price, consumption))
    mean_dict = {}
    for key in price_list[0].keys():
        mean_dict[key] = sum(d[key] for d in price_list) / len(price_list)
    return mean_dict

def calculate_tariff(price, consumption):
     return {
         'unit_price': price.unit_price,
         'grid_fees': price.grid_fee,
         'kwh_price': price.kwh_price,
         'total_price': price.unit_price + price.grid_fee + round(price.kwh_price * consumption,2)
     }

# @bp.get("/get/user/price/async")
# @jwt_required()
# async def async_posts_api_call() -> str:
#     """
#     Calls two endpoints from an external API as async demo
#
#     Returns
#     -------
#     str
#         A JSON object containing the prices
#     """
#     urls = [
#         "https://jsonplaceholder.typicode.com/posts",
#         "https://jsonplaceholder.typicode.com/posts",
#         "https://jsonplaceholder.typicode.com/posts",
#         "https://jsonplaceholder.typicode.com/posts",
#         "https://jsonplaceholder.typicode.com/posts",
#     ]
#
#     async with ClientSession() as session:
#         tasks = (session.get(url) for url in urls)
#         user_posts_res = await asyncio.gather(*tasks)
#         json_res = [await r.json() for r in user_posts_res]
#
#     response_data = {"prices": json_res}
#
#     return response_data, 200
