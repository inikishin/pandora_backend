from api.pandora.base_requests import post, get_record
from api.pandora.config import SYNC_TREE


def sync(target: str, target_object: str, data):
    # actions
    # 1. удаляем в целевой базе записи, которых нет в источнике
    #   1.1 Получаем все записи с цели
    #   1.2. Получаем все записи в источнике
    #   1.3. Проходимся циклом по записям источника, удаляя из целевого массива, записи, по которым идем
    #   1.4. Все, что останется - удаляем

    print('add delete')

    # 2. Экспорт данных в целевую базу
    #   2.1. Получаем все записи в источнике
    #   2.2. Делаем пост запрос по всем записям. Они либо создадутся, либо обновятся

    foreign_keys = SYNC_TREE[target]['objects'][target_object]['foreign_keys']

    for item in data:
        target_item = item.copy()
        for column in item.keys():
            if column in foreign_keys.keys():
                target_record = get_record(target=target, target_object=foreign_keys[column]['linked_object'], external_id=item[column])
                target_item.pop(column)
                target_item[foreign_keys[column]['target_column_name']] = target_record['id']

        print('target_item', target_item)
        post(target=target, target_object=target_object, data=target_item)


from quote.models import Currency, StockExchange, MarketType, Market
def test():
    c = Currency.objects.all().values()
    s = StockExchange.objects.all().values()
    t = MarketType.objects.all().values()
    m = Market.objects.all().values()

    sync('PCM', 'quotes.currency', c)
    sync('PCM', 'quotes.stockexchange', s)
    sync('PCM', 'quotes.markettype', t)
    sync('PCM', 'quotes.market', m)
