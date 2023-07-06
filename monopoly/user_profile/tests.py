from django.test import TestCase
from django.urls import reverse
import pytest
from pytest_django.asserts import assertQuerySetEqual
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate

from .models import Commentary, Profile

# Create your tests here.


@pytest.mark.urls('user_profile.urls')
def test_root_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.urls('user_profile.urls')
def test_root_page_has_navigation_bar(client):
    """Checks whether root page has links of the navbar"""
    response = client.get('/')
    for link in [reverse("index"), reverse("top_players"), reverse('recent_games'), reverse('support_page')]:
        assert link.encode('ascii') in response.content  # Converting link into binary


@pytest.mark.django_db
def test_posting_comments_on_user_page(client):
    new_user = AuthUser.objects.create_user(username="User1", password="User1")
    new_user.save()
    user_one = Profile.objects.create(auth_user=new_user, user_bio='Bio', experience=128, wins=4, losses=8)

    new_user = AuthUser.objects.create_user(username="User2", password="User2")
    new_user.save()
    user_two = Profile.objects.create(auth_user=new_user, user_bio='Bio', experience=128, wins=4, losses=8)

    response_no_comments = client.get(reverse("user_page", kwargs={"id": user_one.pk}))
    assert len(response_no_comments.context["comment_list"]) == 0

    Commentary.objects.create(owner=user_two.auth_user, on_page=user_one.auth_user, content="Comment 1")
    Commentary.objects.create(owner=user_two.auth_user, on_page=user_one.auth_user, content="Comment 2")
    Commentary.objects.create(owner=user_two.auth_user, on_page=user_one.auth_user, content="Comment 3")
    # Next comment is on other person's page
    Commentary.objects.create(owner=user_one.auth_user, on_page=user_two.auth_user, content="Comment on other page")

    response_three_comments = client.get(reverse("user_page", kwargs={"id": user_one.pk}))
    db_three_comments = Commentary.objects.filter(on_page=user_one.auth_user)

    response_one_comment = client.get(reverse("user_page", kwargs={"id": user_two.pk}))
    db_one_comment = Commentary.objects.filter(on_page=user_two.auth_user)

    assertQuerySetEqual(response_three_comments.context["comment_list"], db_three_comments, ordered=False)
    assertQuerySetEqual(response_one_comment.context["comment_list"], db_one_comment, ordered=False)


@pytest.mark.django_db
def test_registering_new_user(client):
    client.post(reverse("register"), {"username": "User1", "password": "securepassword1"})
    valid_user = AuthUser.objects.get(username="User1")
    assert valid_user
    assert Profile.objects.get(auth_user=valid_user)

    client.post(reverse("register"), {"username": "User2", "password": "insecurepassword"})
    try:
        invalid_user = AuthUser.objects.get(username="User2")
    except:
        invalid_user = None
    try:
        invalid_profile = Profile.objects.get(auth_user=invalid_user)
    except:
        invalid_profile = None
    assert not invalid_user
    assert not invalid_profile


@pytest.mark.django_db
def test_logging_in_user(client):
    response = client.post(reverse("register"), {"username": "User1", "password": "securepassword1"})
    valid_user = AuthUser.objects.get(username="User1")
    assert (response.context["user"] == valid_user)
