from app.seed.courts_data_fetching_status_table.courts_data_fetching_status_table import (
    run_create_fetching_courts_data_status_table,
)
from app.seed.lambda_status_table.lambda_status_table import run_lambda_status_table
from app.seed.tenis4u_available_courts_table.tenis4u_available_courts import (
    run_get_tenis4u_available_courts,
)

if __name__ == "__main__":
    run_get_tenis4u_available_courts()
    run_create_fetching_courts_data_status_table()
    run_lambda_status_table()
