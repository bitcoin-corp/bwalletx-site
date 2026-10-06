# 014 · One feed for BSV

Subtitle: Every BSV social app keeps its own feed. bChat shows all of them, credits them, and pays the people who wrote the posts.

Date: October 2026 (draft — not published)

## The odd thing about BSV social apps

Everything you post on Twetch, Treechat, Peck or Fwetch goes on-chain. It's public. Anyone can read it.

And yet each app only shows its own posts. You need a separate app, account and wallet for each one, and a writer on one app never reaches the readers on another.

That's a Web2 habit. On Twitter or Reddit the company owns the posts, so walling them in makes sense for the company. On BSV nobody owns the posts except the people who wrote them. The walls are only around the indexers.

## What bChat does

bitcoinchat.online/feed shows posts from Twetch, Treechat, Peck, Fwetch and bChat in one timeline.

- Every post has a badge saying where it came from, and a link back to the original.
- You can like, reply and tip from bChat. Your reply is a bChat post that points at the original; we never post as another app.
- Tips go straight to the author's own address. bChat takes nothing.

## Authors first

The rule we've written down is simple: a post belongs to the person who wrote it, not to the app they wrote it in.

- Any app can show any author's post, with credit and a link home.
- Authors get paid wherever their post is read.
- If an author hides their own post (a signed "hide" from the same key), every app that follows the spec hides it.
- An app can't stop another app showing public posts. If it wants something kept private, it can keep it off-chain.

## Apps get paid too

When a bChat user tips a post that came from another app, bChat adds 5% on top for that app, in the same transaction. The author still gets the full tip.

So a $0.05 tip on a Treechat post pays the author $0.05 and Treechat $0.0025. Treechat earns from its posts being read in bChat without doing anything.

That's the bit I think the other apps haven't seen yet. Syndication isn't someone taking your content. It's your content earning in more places.

## What we need from the other apps

Two small things:

1. **A payment address for each author on each post.** Some apps post everything from one shared address, so a tip can't reach the right person. That's why tips on Treechat posts are switched off in bChat for now.
2. **A payment address for the app itself**, for the 5% share.

And if they want to show bChat posts back, with a bChat badge, it's one line of code.

## Join

The format is an open spec: bitcoinchat.online/docs/feed-protocol

There's a free public indexer and a drop-in embed:

```html
<script src="https://www.bitcoinchat.online/embed/feed.js" data-source="all"></script>
```

If you build a BSV app with a feed, come and talk to us in the bWallet Lounge on bChat, or email support@bwalletx.com.

— Richard
