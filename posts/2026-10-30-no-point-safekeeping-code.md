---
title: There's No Point Safekeeping Code
date: 2026-11-03
description: Safekeeping code made sense when rebuilding it cost a million dollars. Compaq paid that in 1982. Cloudflare paid $1,100 for the same kind of job in 2026. What the lock protects now is not what it used to.
---

This website is public. Not just the pages. The generator that builds them, every function, every workaround, sits in an open repository for anyone to read. A few years ago that would have felt like leaving the machinery exposed. Lately I notice I don't think about it at all, and I've been trying to work out why.

I think it's this: I no longer believe the code is the part worth protecting. Not because code stopped mattering. Because secrecy was never really protecting the code. It was protected by a price.

## The price was the protection

In 1982, Compaq wanted to sell a computer that ran IBM's software, and the one part they could not copy was the BIOS, the small firmware that made the machine an IBM. So they rebuilt it in a clean room. One team documented what the BIOS did, every behavior, and a second team that had never seen IBM's code wrote new code to match. It took around fifteen programmers, months of work, and about a million dollars. For a piece of firmware you could print out and read in an afternoon.

IBM's protection was never that the rebuilding was impossible, or even that it was illegal. Done cleanly, it was legal. The protection was that almost nobody could afford to do it. Secrecy worked because going around it was irrational. The lock was real. It was just made of money.

## The same job, repriced

In February 2026, Cloudflare published how one of their engineers, directing an AI, reimplemented the API surface of Next.js, the most widely used front-end framework, on top of a different tool. Under a week. About $1,100 in tokens. The result covered 94 percent of the framework's API and was checked against Next.js's own test suite, which is the part that makes it more than a demo. The behavior was the spec, and the tests were the check. Cloudflare calls it experimental, and it was already running in production for customers when they wrote that.

The legal ground had moved before the price finished moving. In 2021 the Supreme Court decided Google v. Oracle, a decade of litigation over Google reimplementing Java's interface for Android. The court sided with Google, and the reasoning is what stayed with me. Justice Breyer wrote that the value of the copied lines lay in the accrued talents of the programmers who had learned them, not in the lines themselves. The interface was worth something because of what people knew. Not because of what the text was.

I am not arguing anyone should go reimplement other people's software. I am watching what happens to a protection when the price underneath it falls by a factor of a thousand. The protection does not get repealed. It gets ignored by economics.

## Both directions at once

I hold both ends of this in my own working life, which is probably why I believe it.

The code for this site is public, all of it. Someone could take the generator tomorrow and have every page I have. What they would not have is a single decision behind it. They would get a sitemap that derives itself and no idea which of the ten ways it broke on a phone taught it to do that.

The platform I built at work is the opposite arrangement. Twenty thousand lines of Python, built from scratch, and I cannot share a line of it. That code is safekept properly, by an employer, behind real walls. And the same fact shows through from this side. If I left, the company keeps every line. What walks out the door is the person who knows why the lines are shaped the way they are, which failure made which check exist. And I could not take the code with me, but give me the behavior and the standards and I could grow it again. I know, because growing it the first time is what I did.

Locked or published, the text turns out to be the part that matters least in both directions. That is not a theory I read. It is the shape of my own week.

## What I actually own

So what is the asset, if it isn't the code? Working it out on this site, it looks like the trail. The versions I rejected. The rendering bug that took a day of bisection on a phone to convict. The conventions I wrote down so the next change would not repeat an old mistake. The standards, the corrections, the taste. It lives in my notes and in my head, and it is the spec behind the spec: the reason the code is this code and not some other code that also passes.

Safekeeping assumed the code was the asset, so you locked the code. I keep my site's code in the open and my judgment in my head, and I couldn't swap those if I tried.

The code was never the thing I owned. I'm getting closer to knowing what the thing is.

*Drafted with an AI's help and edited by me. The examples are documented ones: Compaq's clean-room BIOS is a matter of record, the vinext figures are Cloudflare's own, and the case is Google v. Oracle, decided 2021. Originally published October 30, 2026; revised November 3, 2026.*
