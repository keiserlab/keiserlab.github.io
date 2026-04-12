---
permalink: /
layout: splash
excerpt: "AI and machine learning laboratory at UCSF."
tags: [AI, machine learning, deep learning, generative models, representation learning, drug discovery, systems pharmacology, neuropathology, phenotypic profiling, diffusion models, language models]
header:
   image: /assets/images/bar-network.webp
   image_description: "Keiser Lab network visualization"
#intro: 
#  - excerpt: ''
feature_row:
  - image_path: /assets/images/lab-photo.webp
    alt: "lab lunch"
    title: "Keiser Lab @ UCSF"
    excerpt: "For over a decade, our lab built AI and machine learning for scientific problems we cared about, from drug discovery and neurodegeneration to phenotypic profiling and molecular design. We developed generative, multimodal, and representation learning methods across molecules, images, and biological sequences.


    Michael is now co-founder at [Sygaldry Technologies](https://sygaldry.com), building quantum-accelerated AI."
entries_layout: grid
---

{% include feature_row type="left" %}

{% comment %}{% include feature_row id="intro" type="center" %}{% endcomment %}

{% assign elayout = page.entries_layout | default: 'grid' %}
<div class="entries-{{ elayout }}">
  {% for post in site.posts limit:4 %} 
    {% include archive-single.html type=elayout %}
  {% endfor %}
</div>
