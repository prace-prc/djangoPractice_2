import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

from blog.models import Post


class LatestPostsFeed(Feed):
    title = 'My Blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'

    def items(self):
        return Post.published.all()[:5]

    def items_title(self, item):
        return item.title

    def items_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def items_pubdate(self, item):
        return item.publish
