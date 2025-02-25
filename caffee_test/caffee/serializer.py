from rest_framework import serializers
from .models import Caffe
import json


class CaffeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caffe
        fields = '__all__'

    def validate_table_number(self, value):
        # функция валидации номера стола
        if not isinstance(value, int) or value <= 0:
            raise serializers.ValidationError("Table number must be an integer and positive.")
        return value

    def validate_items(self, value):
        # функция валидации блюда и его цены
        if value is None:
            raise serializers.ValidationError("Items must be provided and cannot be None.")

        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError("Items must be a valid JSON string.")

        if not isinstance(value, dict) or not value:
            raise serializers.ValidationError("Items must be a non-empty dict.")

        for key, val in value.items():
            if not isinstance(key, str):
                raise serializers.ValidationError("All keys in items must be strings.")

            if not (isinstance(val, int) or isinstance(val, float)) or val < 0:
                raise serializers.ValidationError("All values in items must be non-negative numbers.")

        return value

    def validate_total_price(self, value):
        # функция валидации общей стоимости со статусом 'Оплачено'
        if value < 0:
            raise serializers.ValidationError("Total price must be more than zero")
        return value
