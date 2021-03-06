###
# Copyright (c) 2020, mogad0n
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###
### My Libraries

import praw
import time
### Limnoria Libraries

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Redditt')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="",
    username="",
)

class Redditt(callbacks.Plugin):
    """Interact with Reddit using the PRAW library"""
    threaded = True

    def getposts(self, irc, msg, args, opts, sub):
        """ [--num <i>] [--sort <hot|new|controversial|gilded|top|rising>] [<subreddit>]

        Get submissions based on flags provided.
        """
        if sub:
            subreddit = reddit.subreddit(sub)
        else:
            subreddit = reddit.subreddit('TripSit')

        opts = dict(opts)
        if 'num' in opts:
            num = opts['num']
        else:
            num = 10
        if 'sort' in opts:
            if opts['sort'] == 'hot':
                submissions == subreddit.hot(limit=num)
            elif opts['sort'] == 'controversial':
                submissions == subreddit.controversial(limit=num)
            elif opts['sort'] == 'top':
                submissions == subreddit.top(limit=num)
            elif opts['sort'] == 'gilded':
                submissions == subreddit.gilded(limit=num)
            elif opts['sort'] == 'rising':
                submissions == subreddit.rising(limit=num)
            elif opts['sort'] == 'new':
                submissions == subreddit.new(limit=num)
        else:
            submissions == subreddit.new(limit=num)

        for submission in submissions:
            irc.reply(f"\x02 r/{sub or 'Tripsit'}\x0F ::> id: {submission.id} \x1F {submission.title} \x0F by u/{submission.author.name}" 
                f"\x0303 score: {submission.score} \x0F :: comments: {submission.num_comments} :: link: {submission.url} ")

    getposts = wrap(
            getposts,
                [
                getopts(
                    {
                        "num": "int",
                        "sort": ("literal", ("hot", "new", "controversial", "gilded", "top", "rising"))
                    }
                    ),
                    optional("text")
                ]
                )

    def modtools(self, irc, msg, args, opts, identifier):
        """--target <posts|comments> --do <remove|approve|lock|unlock> <id>

        Provides a set of tools for moderating subreddits.
        """
        opts = dict(opts)
        if 'do' not in opts or 'target' not in opts:
            irc.error("Please specify a target and an action using the appropriate format.")
            return
        if opts['do'] == "lock":
            if opts['target'] == 'posts':
                submissions = reddit.submission(id=identifier)
                submissions.mod.lock()
            elif opts['target'] == 'comments':
                comments = reddit.comment(identifier)
                comments.mod.lock()
        elif opts['do'] == "unlock":
            if opts['target'] == 'posts':
                submissions = reddit.submission(id=identifier)
                submissions.mod.unlock()
            elif opts['target'] == 'comments':
                comments = reddit.comment(identifier)
                comments.mod.unlock()
        if opts['do'] == "remove":
            if opts['target'] == 'posts':
                submissions = reddit.submission(id=identifier)
                submissions.mod.remove()
            elif opts['target'] == 'comments':
                comments = reddit.comment(identifier)
                comments.mod.remove()
        elif opts['do'] == "approve":
            if opts['target'] == 'posts':
                submissions = reddit.submission(id=identifier)
                submissions.mod.approve()
            elif opts['target'] == 'comments':
                comments = reddit.comment(identifier)
                comments.mod.approve()
        irc.replySuccess()

    modtools = wrap(
            modtools,
                [
                getopts(
                    {
                        "target": ("literal", ("posts", "comments"))
                        "do": ("literal", ("lock", "unlock", "remove", "approve"))
                    }
                    ),
                    "something"
                ]
                )
    
Class = Redditt


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
