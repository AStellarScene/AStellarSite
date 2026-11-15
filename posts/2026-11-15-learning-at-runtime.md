---
title: Learning at Runtime
date: 2026-11-15
description: I learned radar signal processing by building a radar device and asking questions at the moment each problem appeared. It is the opposite of studying first, and it is much faster.
---

I started building a radar device knowing almost nothing about radar. The job I gave it was simple to say: tell me whether someone is in the room, where they are, and whether they are breathing. No camera, no wearable, just radio energy and whatever I could pull back out of it. I assumed I would have to study the field first and build second. That is not what happened.

## Blocked, in order

Time of flight came first because it had to. Send energy out, time what comes back, and you get distance. That worked, and then it didn't. The steps were too coarse, and a chest rising a few millimetres as someone breathes fell between them. The device could tell me a person-shaped thing was three metres away. It could not tell me the person was alive.

So I had to learn phase. The small motion I needed was not in the range at all. It was in the phase of the returning signal, shifting back and forth as the chest moved. Once I could read that, the device could find a breathing person in a still room.

Direction came last. Distance and breathing gave me a presence on a line, not a position. Phase compared across antennas gave me angle of arrival, and angle plus distance is azimuth. Now the device could place someone instead of just detecting them. Every term I learned arrived as a repair for the last one's failure. It was not a curriculum. It was a list of things broken, in the order they broke.

## The other way

Someone posted a method this week for learning an unfamiliar subject in 48 hours with AI, built on MIT course material. It starts with a corpus, assembled before any questions get asked: six classic textbooks, fifteen research papers, the full set of lecture notes. Then it asks only three things.

First: what does the field agree on? Not a summary. The settled core, laid out as concepts, principles, and the framework that connects them. A map of the subject.

Second: what does the field still argue about? The long-standing disputes, with the reasoning behind each side. The point is not the topics. It is learning where the edges of the field are, and why reasonable people hold opposite positions at them.

Third: an exam. Twenty questions generated from the subject's own exams and homework. Then everything closes. You answer from memory, the AI grades each question, and the grading separates what you memorized from what you actually understood.

The rule under all of it is that the AI is not there to make the subject easier. It does not summarize things down for you. It raises the difficulty: it makes you compare, judge, recall, produce something, and take the correction. Their closing line is that the AI draws the map, and you walk it yourself.

It is a good method. I did almost none of it. I never drew the map. I walked, and the map is whatever is left behind.

## A class of one

People have started calling this personal superintelligence, and I think the name fits. I am learning ten times faster than I ever have, and it is not because the answers got better. It is because there is no gap between the learning and the use. In school I studied things weeks before I touched them, and half of it was gone by the time I did. Here the idea shows up inside the problem, I use it within the hour, and the hardware tells me whether I got it right.

What I notice now is that my way obeyed their one rule by accident. Nothing was summarized for me, and the exam never closed, because the exam was the device. A formula I had only memorized failed exactly the way a wrong one did. The hardware only passes what you actually understand.

A textbook teaches radar to everyone at once. This taught it to one person, in the order my project demanded, against my constraints. A class of one.

Radar is not the point, either. The loop does not care what the subject is. Give it a real thing that pushes back and it teaches me whatever that thing requires. That is the part that changed how I think about learning: the constraint was never whether I could learn a field. It was only ever what I chose to build.

And it worked. The device sits in a room now and does the job I gave it, in the rough way first versions do everything. It finds a person, places them, and reads their breathing out of a signal I could not have parsed a word of when I started.

## The gaps

What I know is shaped exactly like this project. There are whole parts of radar I have never touched because nothing I built ever broke for lack of them. The second question in that post exists to mark the edges of a field on purpose. Mine are unmarked, and I won't pretend otherwise.

But unmarked is not the same as unreachable. Every gap is just a subject I have not pointed this at yet. If the device needed one of them tomorrow, I would learn it the way I learned the rest: inside the problem, against the hardware, in days instead of a semester. The shallowness is a default, not a limit.

Their method can tell you precisely what you don't know before you start. Mine tells me as I go. I have made my peace with that trade, because everything mine knows has already been used for something real.

I wonder what to point it at next.
