<!--
.. title: Easter eggs in your code with invisible text
.. slug: easter-eggs-with-invisible-text
.. date: 2025-10-31 17:18:17 UTC-03:00
.. tags: humor, easter-egg, gist
.. category: scripts
.. link:
.. description:
.. type: text
-->

According to (spanish) Wikipedia, [an "easter egg" is](https://es.wikipedia.org/wiki/Huevo_de_Pascua_(virtual))

> ... is a hidden message or capability embedded in movies, television series, ..., software programs, or video games. Among programmers, there seems to be a drive to leave a personal mark, almost an artistic touch on an intellectual product that is by nature standard and functional. These days, Easter eggs aim to entertain, seek new job opportunities, pay tribute to executives, or amuse programmers.

I have no idea who convinced that gullible Wikipedian that software is "standard and functional", but it is true that the urge for software Easter eggs is almost as old as software itself.

Here is a technique I discovered back in kindergarten, when we would draw with lemon juice so that later, magically, the scribble would be revealed by the teacher's lighter (she was probably smoking in the blocks' corner).

So let’s see how to write invisible (digital) text: lemon juice’s Unicode counterpart.

<!-- TEASER_END -->

## What are zero-width characters?

There is a group of special Unicode characters that occupy no visible space. The most common ones are:

| Code | Name | Description |
|:-----|:-----|:------------|
| `U+200B` | Zero Width Space (ZWSP) | behaves like an “invisible” space |
| `U+200C` | Zero Width Non-Joiner (ZWNJ) | prevents joining characters in some scripts |
| `U+200D` | Zero Width Joiner (ZWJ) | does the opposite: forces characters to join |

These non-printing characters are used, for example, in typesetting systems as control characters or to compose ligatures in alphabets such as Persian or Arabic.

But we can abuse their invisibility and give them a different purpose: use them as bits to encode the sequence of characters of our (visible) text.

If we take any text, convert it to bytes (UTF-8), then to bits, and finally replace each bit with the corresponding character, we end up with a string of invisible characters. When we decode it again, we recover the original message. We can define, for example, that

- ZWSP → `0`
- ZWNJ → `1`

That way we can **embed invisible messages** in comments, strings, or at the end of files without breaking anything. It is a humble steganography trick.

## Minimal example in Python 🐍

This snippet shows how to go from text → sequence of invisible characters → text again:

```python
ZW0 = "\u200b"  # Zero Width Space -> bit 0
ZW1 = "\u200c"  # Zero Width Non-Joiner -> bit 1


def encode_to_zw(text: str) -> str:
    return ''.join(f"{byte:08b}" for byte in text.encode()).translate(
        str.maketrans("01", ZW0 + ZW1)
    )

def decode_from_zw(zw_text: str) -> str:
    bits = zw_text.translate(str.maketrans(ZW0 + ZW1, "01"))
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8)).decode("utf-8", errors="ignore")

secret = "🎵 Hidden music"
payload = encode_to_zw(secret)
print("Invisible payload:", payload)   # looks empty
print("Recovered:", decode_from_zw(payload))
```

Output:

```
Invisible payload: ​‌​‍ ...
Recovered: 🎵 Hidden music
```

So how do you use it as an Easter egg?

1. Generate your invisible payload with the snippet above.
2. Paste it at the end of an innocent comment or line in your code:
   ```python
   # NOTE: nothing to see here. ​‌​‍ ...
   ```
3. Only whoever knows the trick—or investigates it (maybe the other person reading this blog)—will be able to recover it with the decoding script.

## Automate it and go bigger

The manual method is fine for playing around, but if you want to hide messages across many files or search for them throughout an entire repository, a more powerful script helps.

So I asked my <strike>friend</strike> intern LLM to help me build a tool I called [zw_secret.py](https://gist.github.com/mgaitan/53c3b2988b7e6e7a7c2215e0bee8138b).

- Injects invisible messages into one or more files (`zw_secret inject -m "message"`).
- Decodes them from files or entire directories (`zw_secret decode path/`).
- Uses `re` and `concurrent.futures` to scan large codebases quickly.

I'll leave it to you to decode this innocent-looking message:

<script src="https://gist.github.com/mgaitan/d5bdb88a10dfa6b65f10c3e41a269651.js?file=example.txt"></script>

```console
wget https://gist.github.com/mgaitan/d5bdb88a10dfa6b65f10c3e41a269651/raw/01a2e33154384bf47ae256aa72b25f05e8c112ae/example.txt
uv run https://gist.githubusercontent.com/mgaitan/53c3b2988b7e6e7a7c2215e0bee8138b/raw/e253f635f65d97de72d856ad240b45c3192438b4/zw_secret.py decode example.txt
```


PS: This is more of a joke (or a technique for making them). Don't abuse it by putting long messages in your work project, as you'll introduce noise and greatly increase file sizes.
