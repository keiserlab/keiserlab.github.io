---
title: Lab
permalink: /people/
tags: [members, people]
modified: 
comments: false
header:
   image: /assets/images/bar-network.png

layout: archive
collection: people
entries_layout: grid    # list (default), grid
show_excerpts: true     # true (default), false
sort_by: title          # date (default) title
sort_order:             # forward (default), reverse
---

{% comment %} https://github.com/mmistakes/minimal-mistakes/issues/414 {% endcomment %}
<section class="page__content cf">
<h2>Members</h2>
{% assign coll1 = site.people | where: 'type', 'member' %}
<div class="entries-{{ page.entries_layout }}">
  {% include people-list.html entries=coll1 sort_by=page.sort_by sort_order=page.sort_order type=page.entries_layout %}
</div>
</section>

<section class="page__content cf">
<h2>Alumni</h2>
{% assign coll2 = site.people | where: 'type', 'alumn' %}
<div class="entries-{{ page.entries_layout }}">
  {% include people-list.html entries=coll2 sort_by=page.sort_by sort_order=page.sort_order type=page.entries_layout %}
</div>
</section>

