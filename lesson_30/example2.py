from bs4 import BeautifulSoup

html_content = """

<html>
<head>
    <title>example page</head>
</head>
<body>
     <h1>wellcome to beautiful soup<h1>
     <p class="intro">beautiful soup makes web scraping easy</p>
     <div id="content">
     <p>here are some links:</p>
     <a href="http://example.com/page1">link 1</a>
     <a href="http://example.com/page3">link 3</a>
     <a href="http://example.com/page2">link 2</a>
     </div>
</body>
</html>
"""


soup = BeautifulSoup(html_content,'html.parser')

print("title of the page",soup.title.text)

intro_text = soup.find('p',class_='intro').text
print('intro text',intro_text)

#example 3

div_content = soup.find('div',id='content')
links = div_content.find_all('a')
for link in links:
    print("link:",link['href'])


# #example 4

# firs_link = soup.find('a')
# print('first link',firs_link.text)
# print('next sibiling of the first link',firs_link.next_sibiling)


#example 5
paragraphs = soup.select('div#content tent p')
for paragraph in paragraphs:
    print("paragraph inside",paragraph.text)

#example6
new_tag = soup.new_tag('b')
new_tag.string = "important"
soup.h1.append(new_tag)
print("modefies h1",soup.h1)