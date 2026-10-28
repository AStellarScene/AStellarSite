---
title: This site is generated
date: 2026-10-28
description: Every page on this site comes out of a single Python program. As of today the blog does too — this post is the proof and the explanation.
---

There is no CMS behind this site, and no build server. Every page — the home page, the projects, the bookshelf, the Dreamscape, the Atlas — is written out by one Python program. I change the program, run it, and push what it produces. If a page looks wrong, the bug is in the generator, and fixing it there fixes it everywhere.

The Atlas is the clearest example. Nobody places those points by hand. The generator reads the site's own content — every photo, book, artwork, and project — and puts a point in the nebula for each one. Add a book to the shelf and the map grows a point the next time the site builds.

This blog runs on the same rails, and this is the first post through the pipe. A post is just a Markdown file with a title and a date. The generator turns it into a page, lists it here, adds it to the RSS feed and the sitemap, and gives it a point in the Atlas's new Writing cluster. Nothing is registered or copy-pasted anywhere by hand, which matters, because hand-maintained lists go stale silently.

Short notes and longer essays will both land here. First one had to be about the plumbing.

*Drafted with an AI's help and edited by me — the same way most of this site gets built.*
