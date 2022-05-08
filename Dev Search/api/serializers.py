from rest_framework import serializers
from project.models import Project, Tag, Review
from user.models import Profile


class ProfileSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'name', 'email', 'username', 'location', 'short_intro', 'bio', 'profile_image', 'social_github',
                  'social_stackoverflow', 'social_linkedIn', 'social_website', 'social_instagram', 'created', 'id')


class ReviewSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('owner', 'project', 'body', 'value', 'created', 'id',)


class TagSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'created', 'id')


class ProjectSerailizer(serializers.ModelSerializer):

    owner = ProfileSerailizer(many=False)
    tags = TagSerailizer(many=True)
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
        # fields = ('id','title','description','demo_link','featured_image','source_code','vote_count','vote_ratio','created','owner','tags')

    def get_reviews(self,obj): #self refer to serailzer class
        reviews = obj.review_set.all()
        serializers = ReviewSerailizer(reviews,many=True)
        return serializers.data
         