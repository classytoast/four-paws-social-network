from django.test import TestCase, RequestFactory

from groups.models import Group, GroupMember
from pet_owners.models import Owner, Animal, AnimalCategory
from posts.models import Post, GroupPost, OwnerPost, PostImage
from comments.models import PostComment
from posts.utils import *


class GetDataForPosts(TestCase):
    utils_mixin = PostDataMixin()

    @classmethod
    def setUpTestData(cls):
        user = Owner.objects.create(username='simple_user', password='12345')
        user2 = Owner.objects.create(username='simple_user2', password='12345')

        post1 = Post.objects.create(author=user,
                                    title='simple_title',
                                    text_of_post='simple_text')
        post2 = Post.objects.create(author=user, text_of_post='simple_text2')
        post3 = Post.objects.create(author=user, text_of_post='very looooooooooooooooooooooooooooooooong text')
        post4 = Post.objects.create(author=user,
                                    title='simple_title',
                                    text_of_post='simple_text4')
        post5 = Post.objects.create(author=user, text_of_post='simple_text5')
        post6 = Post.objects.create(author=user, text_of_post='very looooooooooooooooooooooooooooooooong text')

        comment1 = PostComment.objects.create(author=user,
                                              comment='some_comment',
                                              post=post1)
        comment2 = PostComment.objects.create(author=user,
                                              comment='some_comment2',
                                              post=post1)

        post1.likes.add(user)
        post2.likes.add(user)
        post2.likes.add(user2)

        post1_owner = OwnerPost.objects.create(post=post1)
        post2_owner = OwnerPost.objects.create(post=post2)
        post3_owner = OwnerPost.objects.create(post=post3)

        group = Group.objects.create(name_of_group='group1', about_group='some_text')
        post1_group = GroupPost.objects.create(group=group, post=post4)
        post2_group = GroupPost.objects.create(group=group, post=post5)
        post3_group = GroupPost.objects.create(group=group, post=post6)

        image1 = PostImage.objects.create(post=post1)
        image2 = PostImage.objects.create(post=post1)
        image3 = PostImage.objects.create(post=post4)
        image4 = PostImage.objects.create(post=post4)

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.utils_mixin.request = self.factory.get('/')
        self.utils_mixin.request.user = Owner.objects.get(username='simple_user')

    def test_user_likes_the_post(self):
        post = Post.objects.get(pk=1)
        result = self.utils_mixin.get_data_for_posts([post], 'owner-post')
        self.assertTrue(result[str(post.pk)]['is_liked'])

    def test_user_no_likes_the_post(self):
        self.utils_mixin.request.user = Owner.objects.get(username='simple_user2')
        post = Post.objects.get(pk=1)
        result = self.utils_mixin.get_data_for_posts([post], 'owner-post')
        self.assertFalse(result[str(post.pk)]['is_liked'])

    def test_one_img_for_owner_post(self):
        posts = Post.objects.filter(pk__lte=3)
        result = self.utils_mixin.get_data_for_posts(posts, 'owner-post')
        img = Post.objects.get(pk=1).images.first()
        self.assertEqual(img, result[str(1)]['img'])

    def test_all_img_for_owner_post(self):
        posts = Post.objects.filter(pk__lte=3)
        result = self.utils_mixin.get_data_for_posts(posts, 'owner-post', all_images=True)
        self.assertEqual(2, len(result[str(1)]['img']))

    def test_owner_post_without_img(self):
        posts = Post.objects.filter(pk__lte=3)
        result = self.utils_mixin.get_data_for_posts(posts, 'owner-post', all_images=True)
        self.assertEqual(0, len(result[str(3)]['img']))

    def test_one_img_for_group_post(self):
        posts = Post.objects.filter(pk__gte=4)
        result = self.utils_mixin.get_data_for_posts(posts, 'group-post')
        img = Post.objects.get(pk=4).images.first()
        self.assertEqual(img, result[str(4)]['img'])

    def test_all_img_for_group_post(self):
        posts = Post.objects.filter(pk__gte=4)
        result = self.utils_mixin.get_data_for_posts(posts, 'group-post', all_images=True)
        self.assertEqual(2, len(result[str(4)]['img']))

    def test_group_post_without_img(self):
        posts = Post.objects.filter(pk__gte=4)
        result = self.utils_mixin.get_data_for_posts(posts, 'group-post', all_images=True)
        self.assertEqual(0, len(result[str(6)]['img']))

    def test_get_extra_data_from_owner_post(self):
        post = Post.objects.get(pk=1)
        result = self.utils_mixin.get_data_for_posts([post], 'owner-post')
        self.assertTrue('animals' in result[str(post.pk)])
        self.assertTrue('is_admin' in result[str(post.pk)])

    def test_get_extra_data_from_group_post(self):
        post = Post.objects.get(pk=4)
        result = self.utils_mixin.get_data_for_posts([post], 'group-post')
        self.assertTrue('is_admin' in result[str(post.pk)])

    def test_get_comments_count_with_transmitted_params(self):
        post = Post.objects.get(pk=1)
        comments = PostComment.objects.filter(post=post)
        result = self.utils_mixin.get_data_for_posts([post], 'owner-post', comments=comments)
        self.assertEqual(2, result[str(1)]['comments_count'])
        post2 = Post.objects.get(pk=2)
        comments2 = PostComment.objects.filter(post=post2)
        result = self.utils_mixin.get_data_for_posts([post2], 'owner-post', comments=comments2)
        self.assertEqual(0, result[str(2)]['comments_count'])

    def test_get_comments_count_with_none_param(self):
        post = Post.objects.get(pk=1)
        result = self.utils_mixin.get_data_for_posts([post], 'owner-post')
        self.assertEqual(2, result[str(1)]['comments_count'])
        post2 = Post.objects.get(pk=2)
        result = self.utils_mixin.get_data_for_posts([post2], 'owner-post')
        self.assertEqual(0, result[str(2)]['comments_count'])


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

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.utils_mixin.request = self.factory.get('/')
        self.utils_mixin.request.user = Owner.objects.get(username='simple_user')

    def test_for_auth_user_is_admin(self):
        post = Post.objects.get(title='simple_title')
        owner_post = OwnerPost.objects.get(post=post)
        result = self.utils_mixin.get_data_for_owner_post(post, owner_post)
        self.assertTrue(result['is_admin'])

    def test_for_auth_user_is_no_admin(self):
        self.utils_mixin.request.user = Owner.objects.get(username='simple_user2')
        post = Post.objects.get(title='simple_title')
        owner_post = OwnerPost.objects.get(post=post)
        result = self.utils_mixin.get_data_for_owner_post(post, owner_post)
        self.assertFalse(result['is_admin'])

    def test_return_animals(self):
        post = Post.objects.get(title='simple_title')
        owner_post = OwnerPost.objects.get(post=post)
        result = self.utils_mixin.get_data_for_owner_post(post, owner_post)
        animals = [animal.name_of_animal for animal in result['animals']]
        self.assertEqual(['animal1'], animals)


class GetDataForGroupPostTestClass(TestCase):
    utils_mixin = PostDataMixin()

    @classmethod
    def setUpTestData(cls):
        user = Owner.objects.create(username='simple_user', password='12345')
        user2 = Owner.objects.create(username='simple_user2', password='12345')
        group = Group.objects.create(name_of_group='group1', about_group='some_text')
        group_member = GroupMember.objects.create(member=user, group=group, is_admin=True)
        post = Post.objects.create(author=user,
                                   title='simple_title',
                                   text_of_post='simple_text')
        group_post = GroupPost.objects.create(group=group, post=post)

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.utils_mixin.request = self.factory.get('/')
        self.utils_mixin.request.user = Owner.objects.get(username='simple_user')

    def test_for_user_is_admin(self):
        post = Post.objects.get(title='simple_title')
        group_post = GroupPost.objects.get(post=post)
        result = self.utils_mixin.get_data_for_group_post(group_post)
        self.assertTrue(result['is_admin'])

    def test_for_user_is_no_admin(self):
        post = Post.objects.get(title='simple_title')
        self.utils_mixin.request.user = Owner.objects.get(username='simple_user2')
        group_post = GroupPost.objects.get(post=post)
        result = self.utils_mixin.get_data_for_group_post(group_post)
        self.assertFalse(result['is_admin'])
