from enum import Enum

from marshmallow import pre_load, post_dump
# from tetamn_common.responses import common_error


class EnumChoicesMixin(Enum):
    """
    Extends built-in Enum class with additional methods:
    `choices` -> gets all enum values
    `names` -> gets all enum names
    `__eq__`, `__hash__` for comparing with raw strings
    `__str__` for human-readable representation of enums.
    """

    @classmethod
    def choices(cls):
        return [x.value for x in cls]

    @classmethod
    def names(cls):
        return cls._member_names_

    @classmethod
    def names_lower(cls):
        return [x.lower() for x in cls._member_names_]

    def __eq__(self, other):
        if not isinstance(other, (str, type(self))):
            raise NotImplementedError
        return self.value == other

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return str(self.value)


class ExistsMixin:
    """
    Extends model class additional methods:
    `exists` -> checking if record exists in database
    """

    @classmethod
    def exists(cls, item_id):
        """
        Check if exists item by id

        Returns:
            bool: True when exists or False when does not exist
        """

        item_exists = cls.query.filter(cls.id == item_id).scalar()
        return True if item_exists else False


class PrefixKeyFieldMixin:
    @post_dump(pass_many=True)
    def prefix_key_field(self, data, many):
        """ Prefixes entities with `data` key """
        if many:
            return data
        return {'data': data}


class UnwrapDataMixin:
    @pre_load
    def unwrap_envelope(self, data, **kwargs):
        # if not data or 'data' not in data:
        #     common_error.with_error(**get_error(ec.REQUEST_BODY_NOT_PREFIXED_5100)).raise_(422)
        return data['data']


class DataSchemaMixin(PrefixKeyFieldMixin, UnwrapDataMixin):
    pass
