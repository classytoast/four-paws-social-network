from django.test import TestCase, Client

from django.urls import reverse

from comments.models import PostComment
from groups.models import Group
from pet_owners.models import Owner, AnimalCategory, Animal
from posts.models import Post, OwnerPost, PostImage, GroupPost


class TestShowPostView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = Owner.objects.create(username='simple_user', password='12345')

        post1 = Post.objects.create(author=user,
                                    title='simple_title',
                                    text_of_post='simple_text')
        owner_post = OwnerPost.objects.create(post=post1)
        post2 = Post.objects.create(author=user,
                                    text_of_post='very looooooooooooooooooooooooooooooooong text')
        owner_post2 = OwnerPost.objects.create(post=post2)

        comment1 = PostComment.objects.create(author=user, comment='some_comment', post=post1)

    def setUp(self):
        self.client = Client()
        self.auth_user = Owner.objects.get(username='simple_user')
        self.client.force_login(self.auth_user)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('post', kwargs={'post_id': 1, 'type_of_post': 'owner_post'}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('post', kwargs={'post_id': 1, 'type_of_post': 'owner_post'}))
        self.assertTemplateUsed(resp, 'posts/post_page.html')

    def test_view_uses_correct_queryset(self):
        resp = self.client.get(reverse('post', kwargs={'post_id': 1, 'type_of_post': 'owner_post'}))
        qs_for_test = Post.objects.get(pk=1)
        self.assertEqual(resp.context['post'], qs_for_test)

    def test_correct_title_in_context(self):
        resp = self.client.get(reverse('post', kwargs={'post_id': 1, 'type_of_post': 'owner_post'}))
        post = Post.objects.get(pk=1)
        self.assertEqual(resp.context['title'], post.title)

        resp = self.client.get(reverse('post', kwargs={'post_id': 2, 'type_of_post': 'owner_post'}))
        post = Post.objects.get(pk=2)
        self.assertEqual(resp.context['title'], post.text_of_post[:10])

    def test_view_gets_data_for_left_menu(self):
        resp = self.client.get(reverse('post', kwargs={'post_id': 1, 'type_of_post': 'owner_post'}))
        self.assertTrue('left_menu' in resp.context)

    def test_view_gets_data_for_right_menu(self):
        resp = self.client.get(reverse('post', kwargs={'post_id': 1, 'type_of_post': 'owner_post'}))
        self.assertTrue('animals_for_right_menu' in resp.context)

    def test_check_user_saw_the_post(self):
        post = Post.objects.get(pk=1)
        self.assertFalse(self.auth_user in post.views.all())
        resp = self.client.get(reverse('post', kwargs={'post_id': 1, 'type_of_post': 'owner_post'}))
        self.assertTrue(self.auth_user in post.views.all())

    def test_correct_comments_in_context(self):
        resp = self.client.get(reverse('post', kwargs={'post_id': 1, 'type_of_post': 'owner_post'}))
        self.assertTrue('comments' in resp.context)
        comments = PostComment.objects.filter(post=Post.objects.get(pk=1))
        self.assertQuerySetEqual(resp.context['comments'], comments)

    def test_view_gets_data_for_post(self):
        resp = self.client.get(reverse('post', kwargs={'post_id': 1, 'type_of_post': 'owner_post'}))
        self.assertTrue('data_for_posts' in resp.context)

    def test_view_gets_likes_for_comments_for_post(self):
        resp = self.client.get(reverse('post', kwargs={'post_id': 1, 'type_of_post': 'owner_post'}))
        self.assertTrue('likes_for_comments' in resp.context)


class TestCreateOwnerPostView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = Owner.objects.create(username='simple_user', password='12345')
        animal_cat = AnimalCategory.objects.create(category='cat1')
        animal1 = Animal.objects.create(name_of_animal='animal1',
                                        pet_owner=user,
                                        category_of_animal=animal_cat,
                                        about_pet='some_text_about_pet')

    def setUp(self):
        self.client = Client()
        self.auth_user = Owner.objects.get(username='simple_user')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('create_owner_post'))
        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_user_not_auth(self):
        resp = self.client.get(reverse('create_owner_post'))
        self.assertRedirects(resp, '/login/?next=%2Fposts%2Fcreate-owner-post%2F', 302)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('create_owner_post'))
        self.assertTemplateUsed(resp, 'posts/add_post_page.html')

    def test_correct_title_in_context(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('create_owner_post'))
        self.assertEqual(resp.context['title'], "Добавление поста")

    def test_view_gets_data_for_left_menu(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('create_owner_post'))
        self.assertTrue('left_menu' in resp.context)

    def test_view_gets_data_for_right_menu(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('create_owner_post'))
        self.assertTrue('animals_for_right_menu' in resp.context)


class TestCreateGroupPostView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = Owner.objects.create(username='simple_user', password='12345')

        group = Group.objects.create(name_of_group='group1', about_group='some_text')

    def setUp(self):
        self.client = Client()
        self.auth_user = Owner.objects.get(username='simple_user')
        self.group = Group.objects.get(name_of_group='group1')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('create_group_post', kwargs={'group_id': self.group.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_user_not_auth(self):
        resp = self.client.get(reverse('create_group_post', kwargs={'group_id': self.group.pk}))
        self.assertRedirects(resp, '/login/?next=/posts/create-group-post/1', 302)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('create_group_post', kwargs={'group_id': self.group.pk}))
        self.assertTemplateUsed(resp, 'posts/add_post_page.html')

    def test_correct_title_in_context(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('create_group_post', kwargs={'group_id': self.group.pk}))
        self.assertEqual(resp.context['title'], "Добавление поста")

    def test_view_gets_data_for_left_menu(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('create_group_post', kwargs={'group_id': self.group.pk}))
        self.assertTrue('left_menu' in resp.context)

    def test_view_gets_data_for_right_menu(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('create_group_post', kwargs={'group_id': self.group.pk}))
        self.assertTrue('animals_for_right_menu' in resp.context)


class TestAddImgsView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = Owner.objects.create(username='simple_user', password='12345')

        post = Post.objects.create(author=user, text_of_post='simple_text')
        post2 = Post.objects.create(author=user, text_of_post='simple_text2')

        img = PostImage.objects.create(post=post)

    def setUp(self):
        self.client = Client()
        self.auth_user = Owner.objects.get(username='simple_user')
        self.post = Post.objects.get(text_of_post='simple_text')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('add_images_to_post', kwargs={'post_id': self.post.pk,
                                                                     'type_of_post': 'owner_post'}))
        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_user_not_auth(self):
        resp = self.client.get(reverse('add_images_to_post', kwargs={'post_id': self.post.pk,
                                                                     'type_of_post': 'owner_post'}))
        self.assertRedirects(resp, '/login/?next=/posts/1/imgs/owner_post/', 302)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('add_images_to_post', kwargs={'post_id': self.post.pk,
                                                                     'type_of_post': 'owner_post'}))
        self.assertTemplateUsed(resp, 'posts/add_images.html')

    def test_correct_title_in_context(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('add_images_to_post', kwargs={'post_id': self.post.pk,
                                                                     'type_of_post': 'owner_post'}))
        self.assertEqual(resp.context['title'], "Добавление изображений")

    def test_view_gets_data_for_left_menu(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('add_images_to_post', kwargs={'post_id': self.post.pk,
                                                                     'type_of_post': 'owner_post'}))
        self.assertTrue('left_menu' in resp.context)

    def test_view_gets_data_for_right_menu(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('add_images_to_post', kwargs={'post_id': self.post.pk,
                                                                     'type_of_post': 'owner_post'}))
        self.assertTrue('animals_for_right_menu' in resp.context)

    def test_there_is_added_images_in_post(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('add_images_to_post', kwargs={'post_id': self.post.pk,
                                                                     'type_of_post': 'owner_post'}))
        self.assertTrue('added_images' in resp.context)
        added_images = self.post.images.all()
        self.assertQuerysetEqual(resp.context['added_images'], added_images)

    def test_there_no_added_images_in_post(self):
        self.client.force_login(self.auth_user)
        post2 = Post.objects.get(text_of_post='simple_text2')
        resp = self.client.get(reverse('add_images_to_post', kwargs={'post_id': post2.pk,
                                                                     'type_of_post': 'owner_post'}))
        self.assertTrue('added_images' in resp.context)
        added_images = post2.images.all()
        self.assertQuerysetEqual(resp.context['added_images'], added_images)


class TestUpdateOwnerPostView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = Owner.objects.create(username='simple_user', password='12345')
        user2 = Owner.objects.create(username='simple_user2', password='12345')

        animal_cat = AnimalCategory.objects.create(category='cat1')
        animal1 = Animal.objects.create(name_of_animal='animal1',
                                        pet_owner=user,
                                        category_of_animal=animal_cat,
                                        about_pet='some_text_about_pet')

        post = Post.objects.create(author=user, text_of_post='simple_text')
        owner_post = OwnerPost.objects.create(post=post)

    def setUp(self):
        self.client = Client()
        self.auth_user = Owner.objects.get(username='simple_user')
        self.post = Post.objects.get(text_of_post='simple_text')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('edit_owner_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_user_not_auth(self):
        resp = self.client.get(reverse('edit_owner_post', kwargs={'pk': self.post.pk}))
        self.assertRedirects(resp, '/login/?next=/posts/1/edit-owner-post/', 302)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('edit_owner_post', kwargs={'pk': self.post.pk}))
        self.assertTemplateUsed(resp, 'posts/edit_post_page.html')

    def test_correct_title_in_context(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('edit_owner_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.context['title'], "Редактирование поста")

    def test_view_gets_data_for_left_menu(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('edit_owner_post', kwargs={'pk': self.post.pk}))
        self.assertTrue('left_menu' in resp.context)

    def test_view_gets_data_for_right_menu(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('edit_owner_post', kwargs={'pk': self.post.pk}))
        self.assertTrue('animals_for_right_menu' in resp.context)


class TestUpdateGroupPostView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = Owner.objects.create(username='simple_user', password='12345')
        user2 = Owner.objects.create(username='simple_user2', password='12345')

        group = Group.objects.create(name_of_group='group1', about_group='some_text')

        post = Post.objects.create(author=user, text_of_post='simple_text')
        group_post = GroupPost.objects.create(post=post, group=group)

    def setUp(self):
        self.client = Client()
        self.auth_user = Owner.objects.get(username='simple_user')
        self.post = Post.objects.get(text_of_post='simple_text')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('edit_group_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_user_not_auth(self):
        resp = self.client.get(reverse('edit_group_post', kwargs={'pk': self.post.pk}))
        self.assertRedirects(resp, '/login/?next=/posts/1/edit-group-post/', 302)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('edit_group_post', kwargs={'pk': self.post.pk}))
        self.assertTemplateUsed(resp, 'posts/edit_post_page.html')

    def test_correct_title_in_context(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('edit_group_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.context['title'], "Редактирование поста")

    def test_view_gets_data_for_left_menu(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('edit_group_post', kwargs={'pk': self.post.pk}))
        self.assertTrue('left_menu' in resp.context)

    def test_view_gets_data_for_right_menu(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('edit_group_post', kwargs={'pk': self.post.pk}))
        self.assertTrue('animals_for_right_menu' in resp.context)


class TestDeletePostView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = Owner.objects.create(username='simple_user', password='12345')
        user2 = Owner.objects.create(username='simple_user2', password='12345')

        post = Post.objects.create(author=user, text_of_post='simple_text')

    def setUp(self):
        self.client = Client()
        self.auth_user = Owner.objects.get(username='simple_user')
        self.post = Post.objects.get(text_of_post='simple_text')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('delete_post', kwargs={'pk': self.post.pk,
                                                              'type_of_post': 'owner_post'}))

        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('delete_post', kwargs={'pk': self.post.pk,
                                                              'type_of_post': 'group_post'}))
        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_user_not_auth(self):
        resp = self.client.get(reverse('delete_post', kwargs={'pk': self.post.pk,
                                                              'type_of_post': 'owner_post'}))
        self.assertRedirects(resp, '/login/?next=/posts/1/delete-post/owner_post/', 302)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('delete_post', kwargs={'pk': self.post.pk,
                                                              'type_of_post': 'owner_post'}))
        self.assertTemplateUsed(resp, 'posts/delete_post_page.html')

    def test_correct_title_in_context(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('delete_post', kwargs={'pk': self.post.pk,
                                                              'type_of_post': 'owner_post'}))
        self.assertEqual(resp.context['title'], "Удаление поста")

    def test_view_gets_data_for_left_menu(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('delete_post', kwargs={'pk': self.post.pk,
                                                              'type_of_post': 'owner_post'}))
        self.assertTrue('left_menu' in resp.context)

    def test_view_gets_data_for_right_menu(self):
        self.client.force_login(self.auth_user)
        resp = self.client.get(reverse('delete_post', kwargs={'pk': self.post.pk,
                                                              'type_of_post': 'owner_post'}))
        self.assertTrue('animals_for_right_menu' in resp.context)