class Setting:
    def __init__(self, default, validator=None):
        self.default = default
        self.validator = validator
        self.name = None

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if self.validator and not self.validator(value):
            raise ValueError(f"Invalid value '{value}' for configuration.")

        setattr(instance, self.name, value)
