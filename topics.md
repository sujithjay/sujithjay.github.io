{% assign all_tags = '' | split: ',' %}

 {% for post in site.posts %}
    {% for tags in post.tags %}
        {% for tag in tags %}
            {% assign all_tags = all_tags | push: tag %}
        {% endfor %}
    {% endfor %}
{% endfor %}

{% assign all_tags = all_tags | sort %}
{% assign all_tags = all_tags | uniq %}

<ul class="tag-list">
{% for tag in all_tags %}
    {% capture tagname %}{{ tag }}{% endcapture %}
    {% capture tagcase %}{{ tag | upcase }}{% endcapture %}
    <a href="/tag/{{ tagname }}" style="color: #da393f;font-size: 1.2rem;font-weight: 600;letter-spacing: 0.05em;"><code class="highligher-rouge"><nobr>{{ tagcase }}</nobr></code>&nbsp;</a>
{% endfor %}
</ul>
