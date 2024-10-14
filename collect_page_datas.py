import re
from bs4 import BeautifulSoup


def remove_words(text, words_to_remove):
    # Create regex pattern to match exact words to remove
    pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, words_to_remove)))

    # Replace matched words with an empty string
    text = re.sub(pattern, '', text)

    # Remove strings with length less than 2 characters
    text = ' '.join([word for word in text.split() if len(word) >= 2])

    return text.strip()


def contains_special_words(text, special_words):
    for word in special_words:
        if word in text:
            return True
    return False


def contains_only_ul(tag):
    for child in tag.children:
        if child.name and child.name != 'ul':
            return False
    return True


def contains_any_ul(tag):
    return tag.find('ul') is not None


def process_link(driver, link):
    try:
        driver.get(link)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        words_to_remove = ['استخدام', 'توسعه دهنده', 'برنامه‌نویس', 'برنامه‌ نویس']
        special_words = ['اسکرام', 'مستر', 'اسکرام مستر', 'خانم']

        title = soup.find('div', class_="c-jobView__titleText").find('h1').text.strip()

        if contains_special_words(title, special_words):
            driver.back()
            return None, None

        title = remove_words(title, words_to_remove)

        target = soup.find('h4', class_='o-box__title', text='شرح موقعیت شغلی').find_next_sibling()
        res_list = []

        if contains_only_ul(target):
            ul_tags = target.find_all('ul')
            for ul in ul_tags:
                li_tags = ul.find_all('li')
                for li in li_tags:
                    res_list.append(li.text.strip())
            content = ', '.join(res_list)
        elif contains_any_ul(target):
            # Process all the text including <ul> tags and other tags
            ul_tags = target.find_all('ul')
            for ul in ul_tags:
                li_tags = ul.find_all('li')
                for li in li_tags:
                    res_list.append(li.text.strip())
            the_str = ', '.join(res_list)
            content = the_str + target.text.strip()
        else:
            # Process all the text without any <ul> tags
            content = target.text.strip()

        driver.back()

        return title, content
    except Exception as e:
        print(f"error in collecting data: {e}")
        driver.back()
        return None, None
