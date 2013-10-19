===========
Subte-M101P
===========

Translation of M101P - MongoDB for Developers course. Course offered by
`MongoDB University`_.

Contributing
============

Contributing is very easy, just follow these steps:

#. Fork this repository with your GitHub account.
#. Create a new issue assigning yourself the translation of a lesson's files.

   For instance: `#111: "Translate Week 2 | 26-getLastError"
   <https://github.com/MongoDBPeru/subte-m101p/issues/111>`_.

#. Create a "lesson branch" or an "issue branch"::

   $ git checkout -b lesson-or-issue

#. Make changes to the caption files you have assigned yourself::

   $ git commit -am "Completed translation of lesson into Spanish. Resolve #111."
   $ git push origin lesson-or-issue

#. And finally, send the pull request from this new branch in your repository
   to our master branch, noting also the issue that you will close.

   For instance: `#180: "Completed translation of 26-getLastError into Spanish"
   <https://github.com/MongoDBPeru/subte-m101p/pull/180>`_ is a pull request
   that will resolve the issue `#111`_.

.. note::

   The team uses a `Kanban board in Huboard
   <http://huboard.com/MongoDBPeru/subte-m101p>`_ to track and manage
   the assignment of the caption files. Please take it into consideration 
   before you start your contribution.

   Usually, at least one team member will verify and discuss your changes before
   merging, so you may have to do more than one commit per pull request.

.. tip::

   To verify your translations, it is easier to use a video player which can play
   the subtitles alongside the video, such as VLC or Dragon Player. Just make
   sure the video and the subtitle have the same filename or load the .srt file
   manually when playing the video.

.. _MongoDB University: http://education.mongodb.com
.. _#111: https://github.com/MongoDBPeru/subte-m101p/issues/111
