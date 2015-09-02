#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, json, requests
from lxml import html

# Extracts all the text inside a specific HTML node
def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))


def fire():
	ap = argparse.ArgumentParser()
	ap.add_argument("-u", "--url", required=True, help="Thread URL")
	ap.add_argument("-k", "--keywords", required=False, help="Keywords (separated by commas)")
	args = vars(ap.parse_args())

	try:
		data = []
		page = requests.get(args["url"])
		keywords = args["keywords"].split(",")

		tree = html.fromstring(page.text)
		comments = tree.xpath('//span[@class="c00"]')
		
		for comment in comments:
			innerContent = stringify_children(comment)
		
			if any(keyword in innerContent for keyword in keywords):
				data.append(unicode(innerContent).encode('utf8'))

		print json.dumps(data)


	except Exception as e:
		print "Error! {e}".format(e=e)

if __name__ == '__main__':
	fire()