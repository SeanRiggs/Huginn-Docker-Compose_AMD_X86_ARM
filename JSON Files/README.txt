Historical Huginn scenario examples
==================================

These exports are retained for reference, not certified for the current Huginn release.
Importing a scenario does not establish that its feeds, APIs, credentials, or agent types still work.

- twitter-stream-update.json: legacy only. TwitterStreamAgent was retired upstream after the old streaming API shut down; it is not a working new-install recipe.
- coronavirus-news-agents.json: historical pandemic-era feeds and filters; sources and locations need revalidation.
- morrison-co-weather-forecaster.json: location-specific NWS example; review endpoints, headers, extraction rules, and notification addresses.
- shake-rattle-and-roll.json: location-specific USGS monitoring example; review feed URLs and recipients before enabling.
- templenet-blog-rss-feed-creator.json: historical blog/RSS example; recheck the feed/site URLs and output settings.
- trailer-comic-scenario.json: historical trailer/comic example; extraction rules and third-party endpoints can change.

Review every imported agent before enabling it. Replace any example recipients and credentials.
Any output/feed secret embedded in a public export is public, not a private credential; generate your own.
Scenario exports do not constitute a full database backup.

New, tested contributions are welcome: include upstream version, test date, service requirements,
sample events, and safe credential placeholders. See ../CONTRIBUTING.md.
