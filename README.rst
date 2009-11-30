django-fuzzydt
==============

An app which provides two things:

1. A view, suitable for calling from ajax, for parsing "fuzzy" (e.g. natural-language) dates, times, and datetimes.
2. A collection of form fields and widgets which use the view to provide "live" previews and validation of dates and times as they are typed into the browser.


Why?
----

Date/time selection solutions on the web suffer from several common problems:

1. Graphical popup calendars require a bazillion (on average, I counted) clicks to choose a date, particularly if the date is not in the current month.
2. Worse still, most graphical popup calendars make the selection process yet more onerous by presenting miniscule click targets for each day and the month navigation buttons.
3. Time selection widgets are practically nonexistant.
4. Text-input solutions exist but they are all user-hostile in that they require user input to be in a very specific format. Additionally, they do not provide ongoing feedback while the user is typing, which necessitates a game of submit-and-let's-see-if-it's-ok.


How?
----

The heavy lifting is provided by the parsedatetime_ module. Consult their documentation for a list of supported formats.

The widgets rely on jquery and a couple of plugins.


Documentation?
--------------

You must be joking. This is a brain-dump release. Docs when I have time.


MOAR DATETIME!
--------------

The view portion of the app is available in hosted form on Google AppEngine at http://natural-datetime.appspot.com.

Release History
---------------

**Oct 9th 2009**: What is laughably called an "initial release," includes a straight dump of code with no documentations or instructions on how to get it to work. Am releasing for the sake of "releasing early", embracing my stupidity and putting it on display.

.. _parsedatetime: http://code.google.com/p/parsedatetime/


TODO
----

* Packaging
* Making it easy to use the included media.
* Document what external media is used (also that this project requires a customized version of labelify.)
* css examples
* Docs
* Tests
* make hidden SplitFuzzyDateTimeFields work.
* I'm sure, lots more...