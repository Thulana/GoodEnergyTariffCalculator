import os
import click
import pandas as pd
from app import create_app
from app import db

from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.models import Prices

app = create_app()


@app.cli.command("remove_old_jwts")
def remove_old_jwts():
    """
    Scan the database for JWT tokens in the Revoked Token table older than 5 days and remove them.
    """

    # Import within the function to prevent working outside of application context when calling flask --help
    from app.models import RevokedTokenModel

    delete_date = datetime.utcnow() - relativedelta(days=5)

    old_tokens = (
        db.session.query(RevokedTokenModel)
        .filter(RevokedTokenModel.date_revoked < delete_date)
        .all()
    )

    if old_tokens:
        for token in old_tokens:
            db.session.delete(token)

        db.session.commit()

        print(
            "{} old tokens have been removed from the database".format(len(old_tokens))
        )

    else:
        print("No JWT's older than 5 days have been found")

    return old_tokens


@app.cli.command("import_prices")
@click.argument("file_path", nargs=1)
def import_prices(file_path):
    # file_path = os.environ.get("CSV_PATH")
    try:
        df = pd.read_csv(file_path, na_values=[""])
        df.dropna(inplace=True)
        for index, row in df.iterrows():
            record = get_record(row)
            db.session.add(record)
        db.session.commit()
        app.logger.info("Database populated successfully")
    except Exception as e:
        app.logger.error("Error occurred while populating db", e)
        db.session.rollback()


def get_record(row):
    house_no_min = row["house_number"].split("-")[0]
    house_no_max = row["house_number"].split("-")[1]
    return Prices(
        **{
            "postal_code": row["postal_code"],
            "city": row["city"],
            "street": row["street"],
            "house_no_min": house_no_min,
            "house_no_max": house_no_max,
            "unit_price": row["unit_price"],
            "grid_fee": row["grid_fees"],
            "kwh_price": row["kwh_price"],
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
