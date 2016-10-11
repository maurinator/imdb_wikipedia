import urllib2
import bs4
import config
from fs_writer import FSWriter

for i in range(int(config.min_year), int(config.max_year)):
    url = "https://en.wikipedia.org/wiki/" + str(i) + "_in_film"
    print url
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page.read(), 'html.parser')
    output = FSWriter(str(i))
    for child in soup.findAll('a'):
        if '+' not in child.text:
            if child.parent.name == 'i':
                if child.parent.parent.name == 'li':
                    output.write(child.text + ' (' + str(i) + ') \n')
