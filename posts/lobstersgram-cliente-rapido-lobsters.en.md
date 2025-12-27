.. title: Lobstersgram, a fast lobste.rs client on Telegram
.. slug: lobstersgram-cliente-rapido-lobsters
.. date: 2025-12-26 23:02:16
.. tags: telegram, lobsters, python, rss, github-actions, telegra.ph
.. category: projects
.. description: A serverless bot that sends lobste.rs posts to Telegram with clean reading.
.. author: Martín Gaitán

Lobsters ([lobste.rs](https://lobste.rs)) is probably my main source[^1] of tech reading: it is a human-curated feed that prioritizes content quality, with no shady clickbait, abusive ads, or hostile comments. Even though I am not a member (it requires an [invitation](https://lobste.rs/about#invitations)), I strongly identify with its ["old internet" spirit](https://lobste.rs/about).

[^1]: Other parts of my nerdy information diet are [Simon Willison's blog](https://simonwillison.net/) and GitHub's ["trending"](https://github.com/trending).

Yesterday, mostly via ChatGPT on my phone, I built Lobstersgram, a bot that works as a fast Lobste.rs client on Telegram.

Every now and then, if the bot detects new posts, it sends you a short message with an intro and a link to the article copied to [telegra.ph](https://telegra.ph), plus the original source link and the discussion thread on the forum. Why republish on Telegraph? Because it supports [instant view](https://instantview.telegram.org/), which allows preloading the content with a simple, consistent style that is ideal for mobile reading.

If you have Telegram, you can try it at [@lobstersgram_bot](https://t.me/lobstersgram_bot)

Commands:

- `/start` to subscribe
- `/unsubscribe` to stop receiving

(Note: it only runs every 2 hours, so it will reply eventually, but do not expect immediacy.)

Here is a demo I recorded capturing my phone screen (with a notification from the family group included).

<iframe height="660" width="355" src="https://www.youtube.com/embed/wdzIBFYjJ3Y" title="Lobstergram demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<!-- TEASER_END -->

## Looking for a better reading experience

Lobsters offers an "aggregation" RSS feed that contains the links to shared articles but not the content itself. So there is not much difference between a traditional RSS reader and opening the site directly in the browser, which is very simple, where you basically click the article titles you are interested in.

Even though most posts are blog articles without ads and are very lightweight, the user experience still has the cognitive cost of reading in different styles and going back and forth between sources and lobsters. On the other hand, for bad connections like the ones we still have around here (for example, when traveling through Patagonia like I am now), it does not hurt to have the readings already available, whatever the conditions.

Lobstersgram improves this user experience mainly for reading on the phone.

The flow is as follows:

- read the Lobsters RSS
- for each link, extract the main content, i.e. a "dynamic scraping" [^2]
- convert the HTML to Markdown
- build a telegra.ph DOM from the Markdown to create a post programmatically, making a copy of the original article
- with that link, a clipped bit of the Markdown, and the rest of the URLs (original + forum) from the RSS, send a message to each bot subscriber

[^2]: I tried [trafilatura](https://trafilatura.readthedocs.io/) but stuck with the old [readability](https://github.com/buriy/python-readability) because it produced better results when converted to markdown.

## Look mom, no server and no DB (and free!)

Telegram bots work via webhooks (the server "pushes" the message in real time) or long polling, which is the mode we care about: instead of constantly checking for new messages, the bot makes a request to the server that stays open for a bit waiting for an update or timeout, and immediately or, **when it can**, makes another request.

GitHub Actions gives us a (free) basic server (as they say in [Tiranos Temblad](https://www.youtube.com/@TiranosTembladTV), long live the free stuff!) that is more than enough to run a small script for a few minutes. And our bot is exactly that: a simple Python script that does not take long.

The action that triggers the workflow is a cron (schedule, in GitHub Actions jargon), and every 2 hours the bot checks whether it needs to update the subscriber list (added/removed) and whether there are stories to send.

For this to work, we also need minimal data persistence. Where will the bot get the list of users who want to receive updates? And when it reads Lobsters, how does it know which posts were already sent in previous runs?

For that there is a `state.json` and a `subscribers.json`, whose purpose should be self-explanatory.

Telegram does not allow you to send messages to chats that never interacted with the bot. So the flow is:

1. the user sends `/start`
2. the workflow runs in `--sync-subscribers` mode
3. the `chat_id` is added to `subscribers.json`
4. in normal mode, each post is sent to those chats

If someone wants to stop receiving, they send `/unsubscribe` and in the next run they are removed.

Here is a little diagram that summarizes it:

[![](https://mermaid.ink/img/pako:eNq1kj2T2jAQhv_Kjqpkgh2BBdgqbiYfM6ZIlYPmxo2QFlCCJUcflxCG_x75fBxJoEkRVdK-j3Zf7epIpFVIOPH4LaKR-FGLrRNtYyCtTrigpe6ECbAC4WHl0V1Ly7rXlrjH21frRa_XOiziGt7JoK3x19R7G3rsk137gG7INFCr7O5uWXN460Pih9iyzlK0XnDo0ChtthA7JQIOar1IYkrIIcv8wcjMx7WXTq_RPVdO4hkRSkGw8BuSf_HWXLgErjhIazbataK3f3Z2qePlDlXcowJ8RHeAye6qjkOh4PP9PbwBmfYBIQwty7s_4P6pPj0KDH73fzm73RJ4lVCIaTiv_0t3-uwX5spDNC_iv5a_0aTWPiJsnG1vTISMyNZpRXhwEUekxTSP_kiOfaKGhB222BCetkq4rw1pzCndSf_rwdr2fM3ZuN0RvhF7n06Dted__xJ1yTi6DzaaQPi4eMpB-JH8ILwY03xCKZ1M54zNGC3nI3JIUJWPi2JWVjM2ZnNWTYrTiPx8KkvzitFpVbJyXk4ZpUV1-gWC-Rou?type=png)](https://mermaid.live/edit#pako:eNq1kj2T2jAQhv_Kjqpkgh2BBdgqbiYfM6ZIlYPmxo2QFlCCJUcflxCG_x75fBxJoEkRVdK-j3Zf7epIpFVIOPH4LaKR-FGLrRNtYyCtTrigpe6ECbAC4WHl0V1Ly7rXlrjH21frRa_XOiziGt7JoK3x19R7G3rsk137gG7INFCr7O5uWXN460Pih9iyzlK0XnDo0ChtthA7JQIOar1IYkrIIcv8wcjMx7WXTq_RPVdO4hkRSkGw8BuSf_HWXLgErjhIazbataK3f3Z2qePlDlXcowJ8RHeAye6qjkOh4PP9PbwBmfYBIQwty7s_4P6pPj0KDH73fzm73RJ4lVCIaTiv_0t3-uwX5spDNC_iv5a_0aTWPiJsnG1vTISMyNZpRXhwEUekxTSP_kiOfaKGhB222BCetkq4rw1pzCndSf_rwdr2fM3ZuN0RvhF7n06Dted__xJ1yTi6DzaaQPi4eMpB-JH8ILwY03xCKZ1M54zNGC3nI3JIUJWPi2JWVjM2ZnNWTYrTiPx8KkvzitFpVbJyXk4ZpUV1-gWC-Rou)

Both `state.json` and `subscribers.json` are auto-committed inside the workflow from GitHub Actions. This idea of using git as data storage is somewhat inspired by the [Git scraping](https://simonwillison.net/2020/Oct/9/git-scraping/) technique.

CLI usage examples:

```console
uv run python main.py --sync-subscribers
uv run python main.py --max-items 1
uv run python main.py --url https://mgaitan.github.io/posts/ampliando-el-universo-python-con-rust/
```

The `--url` mode is interesting because it processes one or more arbitrary URLs outside the RSS feed. When the GitHub Actions workflow is run manually (or via API), you can pass a list of URLs and it will run in this mode, which arrives the same way but obviously without the forum link:

<img width="568" height="281" alt="image" src="https://gist.github.com/user-attachments/assets/d18e12fc-361c-475e-a1a3-7fd54ea3c835" />

By the way, if you want to force messages to go only to you while developing, export this environment variable, which will take priority over the JSON:

```bash
export TELEGRAM_DEV_CHAT_ID=123456789
```

## What's next?

Probably nothing, but the repo is at [mgaitan/lobstersgram](https://github.com/mgaitan/lobstersgram) and it is all yours to fork. The "markdown to telegra.ph" converter needs some improvements and, as my friend [Alvar Maciel](https://alvarmaciel.gitlab.io/) suggested, the `subscribers.json` file should be encrypted (we can do it via [sops](https://github.com/nhedger/setup-sops)) to avoid exposing any data.

As for potential features, it would be easy to let subscribers define the list of feeds they want to consume, making it a general RSS/Atom reader in Telegram.

It could also work as a minimalist "read it later" app and/or a reading community: we send a URL to the bot and when it runs, it processes everything it received in `--url` mode.

Can you think of anything else?
