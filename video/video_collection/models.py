from django.db import models
from urllib import parse
from django.core.exceptions import ValidationError

# Create your models here.

class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        # defines save function for a video object. it checks that the provided url is actually from youtube, based on different conditions
        # then saves the id of the video to be used in the embeded element on the video list web page
        try:
            url_components = parse.urlparse(self.url)
            if url_components.scheme != 'https' or url_components.netloc != 'www.youtube.com' or url_components.path != '/watch':
                raise ValidationError(f'Invalid Youtube URL {self.url}')
            
            query_string = url_components.query
            if not query_string:
                raise ValidationError(f'Invalid Youtube URL {self.url}')
            
            parameters = parse.parse_qs(query_string, strict_parsing=True)
            parameter_list = parameters.get('v')

            if not parameter_list:
                raise ValidationError(f'Invalid Youtube URL parameters {self.url}')

            self.video_id = parameter_list[0]

        except ValueError as e:
            raise ValidationError(f'Unable to parse URL {self.url}') from e
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video ID: {self.video_id}, Notes: {self.notes[:200]}'