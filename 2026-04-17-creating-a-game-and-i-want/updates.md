---
title: Devlog
permalink: /updates/
---

<div class="content-page">
  <section class="panel">
    <span class="eyebrow">Development Journal</span>
    <h1>Devlog + Project Updates</h1>
    <p class="page-intro">
      This page lists every public update for Trailblazers: lore drops, art reveals, feature experiments,
      design notes, and behind-the-scenes progress reports.
    </p>
  </section>

  <section class="post-grid">
    {% for post in site.posts %}
      <article class="post-card">
        <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time>
        <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
        <p>{{ post.excerpt | strip_html | truncate: 180 }}</p>
        <a class="button" href="{{ post.url | relative_url }}">Read update</a>
      </article>
    {% endfor %}
  </section>
</div>
