""""latex.py

Character translation utilities for LaTeX-formatted text.

Usage:
 - unicode(string,'latex')
 - ustring.decode('latex')
are both available just by letting "import latex" find this file.
 - unicode(string,'latex+latin1')
 - ustring.decode('latex+latin1')
where latin1 can be replaced by any other known encoding, also
become available by calling latex.register().

We also make public a dictionary latex_equivalents,
mapping ord(unicode char) to LaTeX code.

D. Eppstein, October 2003.
source: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252124
License: Python license (http://python.org/doc/Copyright.html)
modified for mab2bib 2005/2006 by Henning Hraban Ramm
"""
import re


# Characters that should be ignored and not output in tokenization
_ignore = set([chr(i) for i in range(32)+[127]]) - set({'\x0d', '\x09', '\x0c'})

# Regexp of chars not in blacklist, for quick start of tokenize
_stoppers = re.compile('[\x00-\x1f!$\\-?\\{~\\\\`\']')

_blacklist = set(" \n\r")
_blacklist.add(None)    # shortcut candidate generation at end of data


def _tokenize(tex):
    """Convert latex source into sequence of single-token substrings."""
    start = 0
    try:
        # skip quickly across boring stuff
        pos = _stoppers.finditer(tex).next().span()[0]
    except StopIteration:
        yield tex
        return

    while 1:
        if pos > start:
            yield tex[start:pos]
            if tex[start] == '\\' and not (tex[pos-1].isdigit() and tex[start+1].isalpha()):
                # skip blanks after csname
                while pos < len(tex) and tex[pos].isspace():
                    pos += 1

        while pos < len(tex) and tex[pos] in _ignore:
            pos += 1    # flush control characters
        if pos >= len(tex):
            return
        start = pos
        # protect ~ in urls
        if tex[pos:pos+2] in {'$$': None, '/~': None}:
            pos += 2
        elif tex[pos].isdigit():
            while pos < len(tex) and tex[pos].isdigit():
                pos += 1
        elif tex[pos] == '-':
            while pos < len(tex) and tex[pos] == '-':
                pos += 1
        elif tex[pos] != '\\' or pos == len(tex) - 1:
            pos += 1
        elif not tex[pos+1].isalpha():
            pos += 2
        else:
            pos += 1
            while pos < len(tex) and tex[pos].isalpha():
                pos += 1
            if tex[start:pos] == '\\char' or tex[start:pos] == '\\accent':
                while pos < len(tex) and tex[pos].isdigit():
                    pos += 1


def make_seq_valid(seq):
    """
    Makes sequence a valid sequence by replacing
    \0 -> \\0
    \a -> \\a
    \b -> \\b
    \t -> \\t
    \f -> \\f
    \n -> \\n
    \r -> \\r
    """
    seq = seq.replace("\0", "\\0")
    seq = seq.replace("\a", "\\a")
    seq = seq.replace("\b", "\\b")
    seq = seq.replace("\t", "\\t")
    seq = seq.replace("\f", "\\f")
    seq = seq.replace("\n", "\\n")
    seq = seq.replace("\r", "\\r")
    return seq


def get_tokens(seq):
    valid_seq = make_seq_valid(seq)
    tokens = tuple(_tokenize(valid_seq))
    tokens_list = []
    for token in tokens:
        token = token.strip()
        if len(token) > 0:
            if token.isdigit():
                digits_list = list(token)
                tokens_list.extend(digits_list)
            else:
                tokens_list.append(token)
    return tokens_list

if __name__ == "__main__":
    # test_seq = "\int_{-\epsilon}^\infty dl\: {\\am e}^{-l\zeta}  \int_{-\epsilon}^\infty dl' {\\rm e}^{-l'\zeta}  ll'{l'-l \over l+l'} \{3\,\delta''(l) - {3 \over 4}t\,\delta(l) \} =0. \label{eq21}"
    test_seq = "\START A=A_zdz+A_{\bar z}d\bar z={dx\over y},\label{Aconn} 1112 \END"
    print(test_seq)
    print(get_tokens(test_seq))
