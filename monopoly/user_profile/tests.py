from django.test import TestCase
from django.urls import reverse
import pytest
from pytest_django.asserts import assertQuerySetEqual

from .models import Commentary, User

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
    user_one = User.objects.create(username='Test1', user_bio='Bio', experience=128, wins=4, losses=8)
    user_two = User.objects.create(username='Test2', user_bio='Bio', experience=128, wins=4, losses=8)
    
    response_no_comments = client.get(reverse("user_page", kwargs={"id": user_one.pk}))
    assert len(response_no_comments.context["comment_list"]) == 0

    Commentary.objects.create(owner=user_two, on_page=user_one, content="Comment 1")
    Commentary.objects.create(owner=user_two, on_page=user_one, content="Comment 2")
    Commentary.objects.create(owner=user_two, on_page=user_one, content="Comment 3")
    # Next comment is on other person's page
    Commentary.objects.create(owner=user_one, on_page=user_two, content="Comment on other page")

    response_three_comments = client.get(reverse("user_page", kwargs={"id": user_one.pk}))
    db_three_comments = Commentary.objects.filter(on_page=user_one)

    response_one_comment = client.get(reverse("user_page", kwargs={"id": user_two.pk}))
    db_one_comment = Commentary.objects.filter(on_page=user_two)

    assertQuerySetEqual(response_three_comments.context["comment_list"], db_three_comments, ordered=False)
    assertQuerySetEqual(response_one_comment.context["comment_list"], db_one_comment, ordered=False)
