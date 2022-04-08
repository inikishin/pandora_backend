from celery import shared_task
from quote.helper import load_quotes_from_csv_file, load_quotes_from_moex_api, load_bonds_list_from_moex


@shared_task
def load_quotes_from_moex_api_task(ticker_code: str, timeframe_code: str) -> int:
    quotes_imported = load_quotes_from_moex_api(ticker_code=ticker_code, timeframe_code=timeframe_code)
    return quotes_imported


@shared_task
def load_quotes_from_csv_file_task(ticker_code: str, timeframe_code: str) -> int:
    quotes_imported = load_quotes_from_csv_file(ticker_code=ticker_code, timeframe_code=timeframe_code)
    return quotes_imported


@shared_task
def load_bonds_list_from_moex_task() -> int:
    bonds_imported = load_bonds_list_from_moex()
    return bonds_imported
