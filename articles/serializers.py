from rest_framework import serializers
from articles.models import Article, Category
from users.models import Info, User

class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Article
        exclude = ("active",)

class ArticleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), many=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    active = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = '__all__'

    def get_active(self, obj):
        if obj.author.groups.filter(name='Moderators').exists():
            obj.active = True
            obj.save()
        else:
            obj.active = False
            obj.save()
        return obj.active

    def create(self, validated_data):
        return super().create(validated_data=validated_data)

class ArticlePublishSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), many=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        # fields = '__all__'
        exclude = ('active', 'thumbnail')
        # fields = ['title', 'description', 'content', 'thumbnail', 'category', 'reason', 'author',]

class ProfilesSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), many=False)
    class Meta:
        model = Info
        exclude = ('show_email', 'show_phone',)