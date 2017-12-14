from sw_excel_parser import items
from sw_excel_parser import engines


class ParserMeta(items.ItemMeta):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        meta_bases = tuple(klass.Meta for klass in cls.mro() if 'Meta' in klass.__dict__)

        cls._meta = type('Meta', meta_bases, {})
        cls.item_class = type('Item', (cls._meta.item_class,), cls._unbound_fields)
        cls.engine_class = type('Engine', (cls._meta.engine_class,), dict(item=cls.item_class))


class DefaultParserMeta:
    engine_class = engines.Engine
    item_class = items.Item


class Parser(metaclass=ParserMeta):
    Meta = DefaultParserMeta

    def __init__(self, *args, **kwargs):
        self.engine = self.engine_class(*args, **kwargs)

    def __getattr__(self, name):
        return self.engine.__getattribute__(name)
