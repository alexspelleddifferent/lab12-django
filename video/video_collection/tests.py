from django.test import TestCase
from django.urls import reverse
from .models import Video

class TestReturns404(TestCase):
    
    def test_request_returns_404_for_nonexistent_video(self):
        # get response from non existent data entry
        response=self.client.post(reverse('video_details', args=(200,)), follow=True)
        # make sure error returned is 404
        self.assertEqual(404, response.status_code)

class TestDetailsShowAllInfo(TestCase):

    def test_details_page_shows_all_info(self):
        # create dummy video entry
        v1 = Video.objects.create(pk="1", name="video 1", notes="example", url="https://www.youtube.com/watch?v=NgRoaD9LNT8")

        # get web details page for dummy data
        response = self.client.get(reverse('video_details', args=(1,)))
        # make sure response contains all dummy data
        self.assertContains(response, "video 1")
        self.assertContains(response, "example")
        self.assertContains(response, "NgRoaD9LNT8")