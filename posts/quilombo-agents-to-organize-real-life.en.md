<!--
.. title: Quilombo: agents for organizing real life
.. slug: quilombo-agents-to-organize-real-life
.. date: 2026-08-19 00:06:35 UTC-03:00
.. tags: agents, mcp, django, LLM, inventory, okf
.. category: projects
.. link:
.. description: An inventory system so AI agents can help you find things in the real world.
.. type: text
.. author: Martín Gaitán
-->

A few days ago I resurrected a project I started more than two years ago [^1]. I was building [a little piece of furniture](https://gist.github.com/user-attachments/assets/044aab2f-23bd-42e6-9a04-99fd918b960b) and couldn't find some hinges that I knew I had somewhere. I looked everywhere until I gave up and bought them again. When I got back from the hardware store, I put the drill batteries on charge and started prompting: "Pick this project back up because I still need it."

[^1]: I started it when ChatGPT launched the feature for [customizing GPTs](https://help.openai.com/en/articles/8554397-creating-and-editing-gpts) with a prompt and the specification of a web API they could interact with. The prehistory of an "agent."

The project is called **Quilombo**, a word from [lunfardo](https://en.wikipedia.org/wiki/Lunfardo), the slang of the Río de la Plata, where it means a mess, a chaotic tangle, or a situation that has gotten out of hand. Quilombo is something like an _agentic inventory management system_: a memory that lets AI agents understand and remember the physical world around you and help you find things in it.

<!-- TEASER_END -->

Let me show you [a real conversation from in my ChatGPT](https://chatgpt.com/share/6a85aaf4-be70-83e9-ad4d-9595873f3da3), which is connected to my Quilombo account.

I'll summarize it in case you couldn't be bothered to click:

— Hey, where's the nail clipper?<br>
— On the bedside table, duh. Where else would they be? [^2]

[^2]: Note that although the original inventory entry was in Spanish, the agent was able to find the item and answer in English. When storing data, the agent usually includes English aliases as well.

The usefulness may seem silly if an object's location is obvious, or if you're one of those obsessive people who always know exactly where you keep everything. But in a library, a workshop, or, say, during your next home move, even if we assign every object a place (and stick to it), it is impossible to remember everything without a system.

I think this is what computers were invented for (which is why in Spain they call them "ordenadores" [organizers] 🤣), along with their companions, databases. But here is the obstacle: to be genuinely useful, these systems need the information they process to be detailed, and even if we somehow generate or obtain it, entering it into a particular structure can be slow and incredibly boring (does the job of "data entry," whose task was filling out forms with data, still exist?). A cost incompatible with maintaining a messy, unstructured household inventory.

But now **AI agents** can save us this tedious part of keeping an inventory up to date: you can tell them what you have, where it is, and how many, if you want, using ordinary words. The agent structures and enriches the information and stores it in Quilombo's database without you needing to know how. That database can then be queried "by hand" (like a classic search engine), but the agent can also query it with semantic flexibility (you search for batteries and it might ask about cells too) and answer you again in natural language.

Another [real example](https://chatgpt.com/share/6a8456eb-e8b0-83e9-97bc-f7d36b901a65), this time for entering data:

— Register the bookshelf in my office. On the first shelf I have Ramalho's Fluent Python, second edition. Also the third edition of Crucial Conversations. There's the Nikon camera and my vape. Oh, and the earbud case. <br>
— Copy that.

If this already sounds useful, add the fact that the most powerful models have vision capabilities, so you can **send it a picture of that cursed drawer** where you still keep the charger for your first Nokia, the credit cards you now use via NFC, and the egg-shaped MP3 player with [`The_Ketchup_Song_Asereje_2002.mp3`](https://www.youtube.com/watch?v=5llcBScGuAE) at 96 kbps, downloaded from Ares. The agent will turn that photo into a bulk Quilombo update without you having to press a single key.

[Quilombo is online](https://quilombo-v1-mgaitan.onrender.com/) (**Warning**: from time to time it may take a minute to wake up because I use Render's _free tier_, which puts the instance to sleep. Why? You already know [why](https://mgaitan.github.io/posts/como-usar-varias-cuentas-de-google-photos-para-ampliar-el-espacio-de-copia-de-seguridad/)). You can create an account and configure your agent via MCP to try it out.

Of course, it is [open source](https://github.com/mgaitan/quilombo/).


## The Oscar test

My father-in-law Oscar also has a little shed, a multipurpose workshop where, with supreme pragmatism and a couple of scraps of wood, he fixes the armrest of a freshly broken computer chair, takes apart the carburetor of his van, or carefully builds [luxury sparrow condos](https://textosypretextos.pages.dev/de-otros/gorriones/).

He spends hours there with the radio on, or sometimes talking on the phone with a friend, while searching and rummaging for the little nut he needs.

Oscar has no idea what an MCP, an API schema, or a vector database is, and he has no reason to learn. But he does know, because he is very curious, how to "ask the AI," or "the Chinese girl" as he nicknamed DeepSeek. A universal, conversational interface (Oscar is certainly good at conversation too) that anyone, in any language, can use.

My father-in-law, and so many other people like him, are the users I have in mind. Artificial intelligence put to work in the service of real life.

## The model: embracing disorder and precision

I designed Quilombo to adapt to the chaos of the world around us, without trying to force the world to adapt to a computer system.

For example: in my workshop I have a cabinet with several shelves, and inside it a red toolbox where I keep more or less all my electronics stuff (the soldering iron, solder, and multimeter, say), but there is also a 24-compartment organizer where I keep components salvaged from whatever junk I take apart.

I could simply inventory "all the electronics stuff is in the red box in the cabinet" and that would already be useful. But later I could come up with a code for each compartment in the organizer, count how many green LEDs I have in compartment A4, and, if I want, tell it whenever I use one so it can update the stock.

In other words, the locations Quilombo recognizes have a tree structure: the compartment is in the organizer, which is in the box, which is on the shelf, which is in the cabinet, which is in the workshop, and it is easy to "fine-tune" the information.

There is a concept outside the location hierarchy: the workspace. An account can have many workspaces (a `Home` workspace is created by default), a workspace could be shared among users, and you can grant access to a particular one to your agent (read-only access, if you want).

Objects, for their part, store a name, aliases, category, description, and free-form attributes. Basically, if the agent has more useful details to send along so it can find the object later, the more the merrier: there is room for all of them.

Books are a special case: the agent can query [Open Library](https://openlibrary.org/developers/api) to get metadata that enriches, effortlessly, the information about the books we inventory. _"Take a look among my books: what short story would you recommend for this rainy evening?"_

# The nerdy details

The above can be more or less summarized in this diagram:

![](/images/quilombo_model.png)

(Now that I see it drawn out, I think this model could be simplified even further!)

The code is a Django monolith with PostgreSQL. It is multi-user, keeps data separate by workspace, and exposes an HTTP API and a "remote" MCP server ([streamable HTTP](https://modelcontextprotocol.io/specification/draft/basic/transports/streamable-http) is the keyword) with OAuth. MCP is the standard that lets a client (ChatGPT, Claude, OpenClaw, or any more or less up-to-date agent) discover the service and learn how to search, read an overview of the inventory, move stock, or make bulk changes.

The web interface is minimal for now and exists to create an account, search the inventory when you've run out of tokens, and connect agents, but the main path is conversation.

<img alt="quilombo-architecture" src="https://mgaitan.github.io/quilombo/_images/quilombo-architecture.png" />

There is also a [skill](https://github.com/mgaitan/quilombo/blob/main/skills/manage-quilombo-inventory/SKILL.md) that helps the agent use the MCP. That is where the recommended conversational policy lives:
search before asserting, distinguish "not registered" from "does not exist," show a draft before making changes, and so on.

## What comes next?

For now, I want to see whether anyone wants to use it, finds it useful, and feels like giving feedback or contributing.

Later, maybe I'll put some money into a server that doesn't go to sleep and register a memorable domain (financial support is welcome via [cafecito](https://cafecito.app/tin_nqn_)), then improve the ascetic (or acetic, it also applies) design it has now. That would also help me get listed in the directory of integrable tools for the main AI "chats."

But I know that neither Quilombo nor the agent ecosystem is mature enough yet for the "Oscars of the world" to install this themselves and use it at home. In the meantime, it is an experiment that lets me learn the foundations of this "agentic" era (I also made my first little attempts with [telegram-acp-bot](https://mgaitan.github.io/telegram-acp-bot/)), and it has me particularly excited.

And hopefully I will always know where the 6 mm drill bit is—the one I can never find.
