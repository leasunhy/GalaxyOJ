from lxml.html.clean import Cleaner

# TODO (leasunhy <leasunhy@gmail.com>): deliberately left for future use
tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8',
        'br', 'b', 'i', 'strong', 'em', 'a', 'pre', 'code',
        'img', 'tt', 'div', 'ins', 'del', 'sup', 'sub', 'p',
        'ol', 'ul', 'table', 'thead', 'tbody', 'tfoot',
        'blockquote', 'dl', 'dt', 'dd', 'kbd', 'q', 'samp',
        'var', 'hr', 'ruby', 'rt', 'rp', 'li', 'tr', 'td', 'th',
        's', 'strike', 'summary', 'details']

cleaner = Cleaner()


def sanitize(html_input):
    return cleaner.clean_html(html_input)

