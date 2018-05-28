import random as r
import string


class Generate(object):
    '''
    This class holds methods to
    generate data from json validator object
    '''
    reserved_keys = ('required', 'type', 'title')

    def get_data(self, json_validation_object):
        if not json_validation_object:
            return dict()

        example = self.generate(json_validation_object)
        return example

    def generate(self, schema):
        json = {}
        for key, value in schema.items():
            if key == 'properties':
                json.update(self.generate(value))
                continue

            if key == 'items':
                json.update(self.generate(value))
                continue

            if key in self.reserved_keys:
                continue

            try:
                _type = value['type']

            except Exception:
                json.update({key: value})
                continue

            if _type != 'object' and _type != 'array':
                json.update({key: self.random(value)})
                continue

            if _type == 'array':
                array = []
                for _ in range(r.randint(0, 5)):
                    array.append(self.generate(value))
                json.update({key: array})
                continue

            if _type == 'object':
                json.update({key: self.generate(value)})
                continue

        return json

    def random(self, value):
        _type = value['type']

        if _type == 'number':
            min_value = value.get('minimum', 0)
            max_value = value.get('maximum', 100)
            num = r.uniform(min_value, max_value)

            multiple_of = value.get('multipleOf', 1.0)
            if multiple_of:
                num = self.round_for_multiple_of(num, multiple_of)
                num = round(num, self._get_decimals_count(multiple_of))
            return num

        if _type == 'integer':
            min_value = value.get('minimum', 0)
            max_value = value.get('maximum', 9)
            return r.randint(min_value, max_value)

        if _type == 'string':
            return ''.join(r.choice(
                string.ascii_uppercase + string.digits) for _ in range(10))

        if _type == 'boolean':
            return r.choice([True, False])

    def _get_decimals_count(self, number):
        return str(number)[::-1].find('.')

    def round_for_multiple_of(self, number, multiple_of):
        return float(multiple_of * round(number/multiple_of))
