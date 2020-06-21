from requests import get
from json import loads
from datetime import datetime, date
from typing import List

class User:
	def __init__(self, username: str) -> None:
		self.username = username
		self.response = get(f'https://instagram.com/{self.username}?__a=1')
		self.data_json = loads(self.response.text)['graphql']['user']

		base_url = 'https://www.instagram.com/graphql/query/?query_id=17888483320059182&id='
		self.all_data = get_json(f"{base_url}{self.data_json['id']}&first=51")
		self.posts_data = self.all_data['data']['user']['edge_owner_to_timeline_media']

		self.posts_data2 = []
		if self.posts_data['page_info']['has_next_page']:
			self.posts_data2 = get_json(f"{base_url}{self.data_json['id']}&first=294&after={self.posts_data['page_info']['end_cursor']}")
			self.posts_data2 = self.posts_data2['data']['user']['edge_owner_to_timeline_media']

		posts_data = self.all_data['data']['user']['edge_owner_to_timeline_media']
		self.requests_list = []
		end_cursor = posts_data['page_info']['end_cursor']

		for _ in range(5):
			try:
				if self.posts_data['page_info']['has_next_page']:
					new_request = get_json(f"{base_url}{self.data_json['id']}&first=294&after={end_cursor}")
					new_request = new_request['data']['user']['edge_owner_to_timeline_media']

					self.requests_list.append(new_request)
					end_cursor = new_request['page_info']['end_cursor']

				else:
					if not self.requests_list:
						self.requests_list.append(posts_data)
					break

			except:
				break

	def is_private(self) -> bool:
		return self.data_json['is_private']

	def get_posts(self) -> List[dict]:
		post_data = []

		for data in self.requests_list:
			for i in range(len(data['edges'])):
				post = data['edges'][i]['node']

				description = '' if not post['edge_media_to_caption']['edges'] \
					else post['edge_media_to_caption']['edges'][0]['node']['text']

				img_url = [post['display_url']]

				request_img = get_json(f"https://www.instagram.com/p/{post['shortcode']}/?__a=1")

				img_data = request_img['graphql']['shortcode_media']

				try: foo = img_data['edge_sidecar_to_children']
				except: pass
				else:
					for img in img_data['edge_sidecar_to_children']['edges']:
						img = img['node']
						if not img['display_url'] in img_url:
							img_url.append(img['display_url'])

				post_data.append({
					'date': normal_time(post['taken_at_timestamp']),
					'post_url': f"https://instagram.com/p/{post['shortcode']}",
					'img_url': img_url,
					'shortcode': post['shortcode'],
					'like_count': post['edge_media_preview_like']['count'],
					'comment_count': post['edge_media_to_comment']['count'],
					'description': description
				})

		return post_data
			

	def filter_by_date(self, posts: str, _from: str, _to: str) -> List[dict]:
		filter_post = [post for post in posts \
			if get_date(_from) <= get_date(post['date']) <= get_date(_to)]

		return filter_post

	def sort_by_like(self) -> List[dict]:
		posts = self.get_posts()
		return sorted(posts, key = lambda post: post['like_count'])[::-1]

	def sort_by_comment(self) -> List[dict]:
		posts = self.get_posts()
		return sorted(posts, key = lambda post: post['comment_count'])[::-1]

# some func for datetime
def normal_time(date: int) -> str:
	return datetime.fromtimestamp(date).strftime('%d.%m.%Y')

def get_date(date_str: str) -> datetime.date:
	date_list = date_str.split('.')

	return date(
		int(date_list[2]),
		int(date_list[1]),
		int(date_list[0])
	)

def get_json(url: str) -> dict:
	try:
		return loads(get(url).text)
	except:
		return get(url).json()