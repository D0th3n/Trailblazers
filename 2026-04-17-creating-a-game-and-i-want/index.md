---
title: Home
---

<section class="hero">
  <div class="panel hero-copy">
    <span class="eyebrow">Worldbuilding In Public</span>
    <h1>Welcome to the world of Trailblazers.</h1>
    <p class="lede">
      This is the official archive for the game's evolving universe: factions, legends, concept drops,
      dev journals, visual experiments, and progress updates as the project takes shape.
    </p>
    <div class="hero-actions">
      <a class="button button-primary" href="{{ '/updates/' | relative_url }}">Read the devlog</a>
      <a class="button" href="{{ '/universe/' | relative_url }}">Explore the lore</a>
    </div>
  </div>

  <div class="panel stats">
    <div class="stat">
      <strong>01</strong>
      <span>Core mission: turn worldbuilding into a public-facing record fans can follow from day one.</span>
    </div>
    <div class="stat">
      <strong>02</strong>
      <span>Posting format: story fragments, development updates, concept art, screenshots, and patch notes.</span>
    </div>
    <div class="stat">
      <strong>03</strong>
      <span>GitHub-native workflow: edit pages and devlog posts as Markdown files, then publish with GitHub Pages.</span>
    </div>
  </div>
</section>

<section>
  <div class="section-heading">
    <div>
      <h2>What this site is built for</h2>
      <p>A small but expandable foundation for a game universe site.</p>
    </div>
  </div>

  <div class="grid-3">
    <article class="feature-card">
      <h3>Lore Library</h3>
      <p>Document places, factions, relics, characters, and timeline events in one home base that grows with the game.</p>
    </article>
    <article class="feature-card">
      <h3>Devlog Publishing</h3>
      <p>Post updates as dated Markdown entries so your community can follow the project as it develops.</p>
    </article>
    <article class="feature-card">
      <h3>Art + Screenshots</h3>
      <p>Drop in concept art or in-game images under <code>assets/images/</code> and feature them in posts or the gallery page.</p>
    </article>
  </div>
</section>

<section>
  <div class="section-heading">
    <div>
      <h2>Latest updates</h2>
      <p>The newest devlog posts appear here automatically.</p>
    </div>
    <a class="button" href="{{ '/updates/' | relative_url }}">View all posts</a>
  </div>

  <div class="post-grid">
    {% for post in site.posts limit:3 %}
      <article class="post-card">
        <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time>
        <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
        <p>{{ post.excerpt | strip_html | truncate: 150 }}</p>
      </article>
    {% endfor %}
  </div>
</section>
