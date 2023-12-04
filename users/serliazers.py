from rest_framework import serializers

from users.models import User, Code


#class UserSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = User
#        fields = '__all__'
#
#
class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ['code',]

    # проверка на пустату в поле code
    def validate_code(self, value):
        if not value:
            raise serializers.ValidationError('Код не может быть пустым')
        return value

