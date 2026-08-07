class ReportFactory:

    registry = {}

    @classmethod
    def register(cls, name):
        def decorator(func):
            cls.registry[name] = func
            return func
        return decorator

    @staticmethod
    def create_object(name, db, data_dict):
        if name not in ReportFactory.registry:
            raise ValueError("No such class in dictionary")
        return ReportFactory.registry[name](db, data_dict)