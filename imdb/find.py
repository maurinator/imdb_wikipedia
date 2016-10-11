import urllib2
import bs4
import config
from fs_writer import FSWriter
search_query = "http://www.imdb.com/find?ref_=nv_sr_fn&q="
end_search = "&s=all"
main = 'http://www.imdb.com'


def parse_url(url):
    new_url = url.replace(" ", "+").replace("(", "%28").replace(")", "%29")
    return new_url


def get_search_url(url):
    return search_query + parse_url(url) + end_search

for i in range(int(config.min_year), int(config.max_year)):
        movie = FSWriter(str(i))
        titles = movie.read_all()
        for title in titles:
            title = title.strip()
            print title
            try:
                page = urllib2.urlopen(get_search_url(title))
                soup = bs4.BeautifulSoup(page.read(), 'html.parser')
                results = soup.findAll('td', {'class': 'result_text'})
                found = False
                for r in results:
                    if title in r.getText().encode('utf-8'):
                        link = r.a['href']
                        search_page = urllib2.urlopen(main + link)
                        page = bs4.BeautifulSoup(search_page.read(), 'html.parser')
                        print page.title.string
                        print (main + link)
                        found = True
                        break
                if found:
                    link_id = link.split('/')[2]
                    reviews = page.findAll('p', {'itemprop': 'reviewBody'})

                    page = urllib2.urlopen(main + '/title/' + link_id + '/plotsummary')
                    soup = bs4.BeautifulSoup(page, 'html.parser')
                    summaries = soup.find_all('p', {'class': 'plotSummary'})

                    f = open('data/' + title.replace('/', '') + '.html', 'w')
                    f.write('<HTML>\n<head>\n')
                    f.write("<title>" + title + '</title>' + '\n')
                    f.write("</head>\n<body>\n")
                    f.write('<h1>' + title + '</h1>' + '\n')

                    if len(summaries) > 0:
                        f.write('<h2> Summaries </h2>' + '\n')
                        for s in summaries:
                            f.write('<p>' + s.getText().encode('utf-8').strip() + '</p>' + '\n')

                    if len(reviews) > 0:
                        f.write('<h2> Reviews </h2>' + '\n')
                        for r in reviews:
                            f.write('<p>' + r.getText().encode('utf-8').strip() + '</p>' + '\n')

                    f.write('</body>\n</html>')
            except urllib2.HTTPError:
                print ("HTTPError handler")
            except urllib2.URLError:
                print ("HTTPURLError")
