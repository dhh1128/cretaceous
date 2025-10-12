# manual-rag

## How to Use
1. **ONCE**: complete initial setup for your project.
   * [Edit `prompts/start_chat.md`](../../edit/main/prompts/start-chat.md). Assign a better title for your project and define the values of the `$gh_user` and `$repo` variables. (If you use manual_rag projects, it may save you some time to ask your AI to add the value of `$gh_user` to its permanent memory about you, instead.)
2. **EVERY TIME YOU WANT TO USE AN AI WITH YOUR PROJECT**: Copy the raw contents of [`prompts/start_chat.md`](prompts/start-chat.md), and paste it into your chat.

## Why?
Some of the most interesting things you can do with AI don't fit well into a single chat. Sure, chats can persist, but it's easy to exceed the AI's context window. Take writing a novel, for example. If you ask an AI to help you write chapter 20, does your prompt have to first give it chapters 1-19 as context? How do you convey to the AI all the worldbuilding that you've done in your imagination, or the backstories of each of the main characters, or the historical context of the milieu? What if you want to use multiple AIs for different parts of the task, and they all need this same context?

## RAG
[RAG (Retrieval-Augmented Generation)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) is a go-to strategy to make AIs handle context more flexibly. Essentially, this is progressive disclosure -- you make the AI aware that more information is available, and instruct it to fetch the subset of that information that's truly needed, on demand. Now your collaboration with AI can become far more complex and nuanced and iterative.

LLMs that are online and public have built-in RAG for common sources; they all know how to look up topics in the equivalent of wikipedia, for example. And [MCP](https://modelcontextprotocol.io/docs/getting-started/intro) lets them consult all sorts of automated interfaces with specialized forms of knowledge, like stock-tickers, sports scores, IMDB-style movie reviews, prices and availability for plane tickets and hotels, and the like.

## Your Custom RAG
But what if the knowledge needed by AI is knowledge that only *you* have? There's no MCP interface for your brain...

This repo documents a strategy for being your own progressively disclosable source of knowledge for an AI. You write down some of what you know, and maybe hint about other stuff you haven't had time to write. This information is persisted in markdown docs on Github. (You can use Github's wiki feature to do this, so you don't have to hand-edit raw markdown.) Your files become a knowledge base that an AI can call upon. You use a careful file naming and hyperlinking convention, and you have automation maintain an accurate table of contents. You teach the AI about the KB, its conventions, and your process, and then instruct the AI to prompt you when it needs more info. Now when you want help writing chapter 20, you can tell it that chapters 1-19 exist, along with your KB of background knowledge. If the AI requests doc X, it will understand the hyperlinks and learn what else it could or should request.
