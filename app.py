import sele, iconsquare_comments, email_manager

import time

def main():

	Email_manager = email_manager.email_manager_class()

	Insta_scrape = iconsquare_comments.scraping()
	Insta_scrape.oper_driver()

	Insta_scrape.login("iconosquare@amomlins.com", "XHm%M6By8ML3")

	Insta_scrape.followers(Email_manager)

	Insta_scrape.list_comments()
	
	Insta_scrape.send_comments_to_email("ptiago1414@gmail.com", Insta_scrape.all_comments_elements, Email_manager)

	Insta_scrape.close()


	time.sleep(5)

main()
