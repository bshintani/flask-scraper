from functions import scrape_pages, step_into_url

scrape_pages('https://security.stackexchange.com/questions/tagged/iot?page=')
scrape_pages('https://security.stackexchange.com/questions/tagged/cloud-computing?page=')
scrape_pages('https://security.stackexchange.com/questions/tagged/mobile?page=')
step_into_url()
