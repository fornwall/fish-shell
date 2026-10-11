#!/usr/bin/env python3
from pexpect_helper import SpawnedProc
import os

env = os.environ.copy()
env["TERM"] = "xterm"

# Use a narrow terminal (24 rows, 20 columns) so that the command line below wraps.
sp = SpawnedProc(env=env, dimensions=(24, 20))
send, sendline, expect_prompt, expect_re, expect_str = (
    sp.send,
    sp.sendline,
    sp.expect_prompt,
    sp.expect_re,
    sp.expect_str,
)
expect_prompt()

sendline("set -g fish_autosuggestion_enabled 0")
expect_prompt()

# "prompt 2>" is 9 columns wide, so this command line is one column too wide to fit on a single
# line, and the two-column emoji wraps to the next line.
send("echo aaaaa😀")
expect_str("😀")

# Move the cursor before the emoji and delete the character before it. The command line now
# shrinks to a single line and the emoji ends exactly in the last column.
send("\x1b[D\x7f")

# Since the screen shrank, fish clears to the end of the screen. It must do so *before* writing
# the emoji into the last column: in terminals where the cursor sticks to the last column, clearing
# afterwards would erase the emoji.
expect_re("\x1b\\[J(\x1b\\[[0-9;]*m)*😀")
