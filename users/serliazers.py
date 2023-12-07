from rest_framework import serializers

from users.models import User, Code
from users.utils import generate_invite_code


class LoginSerializer(serializers.ModelSerializer):
    """
    Сериализатор для аутентификации пользователя по номеру телефона.
    """
    phone = serializers.CharField()

    class Meta:
        model = User
        read_only_fields = ("id",)
        fields = ("id", "phone")

    def create(self, validated_data: dict) -> User:
        """
        Создает пользователя и генерирует 4-значный токен для аутентификации.
        """
        instance, _ = User.objects.get_or_create(**validated_data)

        if instance.referral_code is None:
            instance.referral_code = generate_invite_code()
            instance.save()

        code = Code.objects.create(user=instance)
        code.save()

        return instance


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ['code', ]

    # проверка на пустату в поле code
    def validate_code(self, value):
        if not value:
            raise serializers.ValidationError('Код не может быть пустым')
        return value


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с профилем пользователя.
    """
    referral_code = serializers.CharField(write_only=True, required=False)
    else_referral_code = serializers.CharField(read_only=True, required=False)
    users_with_else_referral_code = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'phone', 'referral_code', 'else_referral_code', 'users_with_else_referral_code']

    def get_users_with_else_referral_code(self, instance):
        """
        Возвращает список пользователей, введенных по чужому инвайт-коду текущего пользователя.
        """
        if instance.else_referral_code:
            users_with_else_referral_code = User.objects.filter(referral_code=instance.else_referral_code)
            return [user.phone for user in users_with_else_referral_code]
        return []

    def validate_referral_code(self, value):
        """
        Проверка на существование инвайт-кода и убеждаемся, что у пользователя нет уже активированного чужого инвайт-кода.
        """
        if value is not None:
            try:
                User.objects.exclude(pk=self.instance.pk).get(else_referral_code=value, referral_code=None)
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid or already used referral code entered.')

        return value

    def update(self, instance, validated_data):
        """
        Обновляет пользователя при вводе чужого инвайт-кода.
        """
        referral_code = validated_data.get('referral_code', None)
        if referral_code:
            if instance.referral_code:
                raise serializers.ValidationError('You can activate the referral code only once.')
            else:
                else_user = User.objects.get(referral_code=referral_code)
                instance.else_referral_code = referral_code
                instance.save()

        return instance
