from app import ma
from app.models import Users, Prices

from marshmallow import Schema, fields


class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users


class UsersDeserializingSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()


class PricesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Prices


class PriceRequestDeserializingSchema(Schema):
    zip_code = fields.Integer(required=True)
    city = fields.String(required=True)
    street = fields.String(required=True)
    house_number = fields.Integer(required=True)
    yearly_kwh_consumption = fields.Float(required=True)
