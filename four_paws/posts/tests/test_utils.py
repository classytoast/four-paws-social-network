from django.test import TestCase, RequestFactory

from groups.models import GroupPostComment, GroupMember, GroupPost
from pet_owners.models import PostComment, OwnerPost, Owner, Animal, AnimalCategory
from posts.models import Post
from posts.utils import *


class GetDataForOwnerPostTestClass(TestCase):
    utils_mixin = PostDataMixin()

    @classmethod
    def setUpTestData(cls):
        user = Owner.objects.create(username='simple_user', password='12345')
        user2 = Owner.objects.create(username='simple_user2', password='12345')
        animal_cat = AnimalCategory.objects.create(category='cat1')
        animal1 = Animal.objects.create(name_of_animal='animal1',
                                        pet_owner=user,
                                        category_of_animal=animal_cat,
                                        about_pet='some_text_about_pet')
        post = Post.objects.create(author=user,
                                   title='simple_title',
                                   text_of_post='simple_text')
        owner_post = OwnerPost.objects.create(post=post)
        owner_post.animals.add(animal1)
        comment1 = PostComment.objects.create(author=user,
                                              comment='some_comment',
                                              post=owner_post)
        comment2 = PostComment.objects.create(author=user,
                                              comment='some_comment2',
                                              post=owner_post)
        post_without_comments = Post.objects.create(author=user, text_of_post='simple_text2')
        owner_post = OwnerPost.objects.create(post=post_without_comments)
        owner_post.animals.add(animal1)

    def setUp(self) -> None:
        self.utils_mixin.request = RequestFactory()
        self.utils_mixin.request.user = Owner.objects.get(username='simple_user')

    def test_for_user_is_admin(self):
        post = Post.objects.get(title='simple_title')
        result = self.utils_mixin.get_data_for_owner_post(post)
        return self.assertEqual(True, result['is_admin'])

    def test_for_user_is_no_admin(self):
        post = Post.objects.get(title='simple_title')
        self.utils_mixin.request.user = Owner.objects.get(username='simple_user2')
        result = self.utils_mixin.get_data_for_owner_post(post)
        return self.assertEqual(False, result['is_admin'])

    def test_return_animals(self):
        post = Post.objects.get(title='simple_title')
        result = self.utils_mixin.get_data_for_owner_post(post)
        animals = [animal.name_of_animal for animal in result['animals']]
        return self.assertEqual(['animal1'], animals)

    def test_return_comments(self):
        post = Post.objects.get(title='simple_title')
        result = self.utils_mixin.get_data_for_owner_post(post)
        return self.assertEqual(2, result['comments_count'])

    def test_return_without_comments(self):
        post = Post.objects.get(text_of_post='simple_text2')
        result = self.utils_mixin.get_data_for_owner_post(post)
        return self.assertEqual(0, result['comments_count'])
