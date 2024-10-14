from bs4 import BeautifulSoup
from pymongo import MongoClient

from selenium.webdriver.common.by import By

from getPage import getPage
from setFilter import set_filter
from collect_page_datas import process_link
from analaysing import analysis


if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    db = client['jobs']
    collection = db['collection_1']

    res, driver = getPage()

    if not res:
        print(driver)
        exit(0)
    print('the page got successfully!')

    res, msg = set_filter(driver)
    print(msg)
    if not res:
        exit(0)

    # all pages loop
    jobs = 0
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_ul_tag = soup.find('ul', {'class': 'o-listView__list c-jobListView__list'})

        if not job_ul_tag:
            print('any job not found')
            exit(0)

        job_li_tags = job_ul_tag.find_all('li')
        links = [li.find('a')['href'] for li in job_li_tags if li.find('a')]
        jobs += len(links)

        try:
            for link in links:
                title, content = process_link(driver, link)

                if title:
                    collection.insert_one(
                        {
                            'title': title,
                            'content': content,
                            'url': link
                        }
                    )

        # use ul_tags to refer
        except Exception as e:
            print(f"An error occurred collecting datas: {e}")

        # now, should to go to next page
        try:
            next_btn = driver.find_element(By.XPATH, '//*[@class="paginator"]').find_elements(By.TAG_NAME, 'li')[-1]
            next_btn.click()
        except:
            print('jobs finished')
            break

    print(f'process finish by {jobs} jobs')

    # now analyse the datas
    analysis()
