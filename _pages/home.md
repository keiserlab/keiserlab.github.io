---
permalink: /
layout: splash
excerpt: "Systems pharmacology and deep learning laboratory at UCSF."
tags: [SEA, machine learning, systems pharmacology, computational chemical biology]
header:
   image: /assets/images/bar-network.png
intro: 
  - excerpt: '*Our lab combines machine learning and chemical biology methods to investigate how small molecules perturb protein networks to achieve therapeutic effects.*'
feature_row:
  - image_path: /assets/images/lab-photo-2.jpg
    alt: "lab lunch"
    title: "Welcome to the Keiser Lab"
    excerpt: "We're part of the [Institute for Neurodegenerative Diseases](http://ind.ucsf.edu), the [Bakar Computational Health Sciences Institute](http://bakarinstitute.ucsf.edu/), the [Department of Pharmaceutical Chemistry](http://pharmchem.ucsf.edu), and the [Department of Bioengineering and Therapeutic Sciences](http://bts.ucsf.edu/).

    We're located in the [Sandler Neurosciences Center](http://www.som.com/projects/university_of_california_san_francisco_sandler_neurosciences_center) at UCSF Mission Bay."
entries_layout: grid
---

{% include feature_row type="left" %}

{% include feature_row id="intro" type="center" %}

{% assign elayout = page.entries_layout | default: 'grid' %}
<div class="entries-{{ elayout }}">
  {% for post in site.posts limit:4 %} 
    {% include archive-single.html type=elayout %}
  {% endfor %}
</div>