This code is a mix of code/ideas from the following tutorials covered by the MIT license:

* https://github.com/mattmakai/fullstackpython.com/blob/gh-pages/source/content/posts/160604-build-first-slack-bot-python.markdown
* https://github.com/mccreath/isitup-for-slack/blob/master/docs/TUTORIAL.md

Follow the steps from  https://github.com/mattmakai/fullstackpython.com/blob/gh-pages/source/content/posts/160604-build-first-slack-bot-python.markdown to get it going.

#Technical notes

* Note that you will have to fill in the actual token and bot id in `set_env.sh` as well as the `BOT_NAME` in `print_bot_id.py`.
* If you see SSH-related errors while running `is_up.py`, you might want to add security package to your virtual environment using `pip install requests[security]`.
