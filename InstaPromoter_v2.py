import mechanize, yaml, re, time, sys, requests, hmac, urllib, json, cookielib, sys
import datetime
from hashlib import sha256


TOP_HASHTAGS_URL = "http://top-hashtags.com/"
TOP_HASHTAGS_HOT = TOP_HASHTAGS_URL + "instagram/1/"

INSTAGRAM_URL = "https://www.instagram.com/"
INSTAGRAM_TAG_URL = INSTAGRAM_URL + 'explore/tags/'
INSTAGRAM_LOCATION_URL = INSTAGRAM_URL + 'explore/locations/'

INSTAGRAM_API = "https://api.instagram.com/v1/media/"
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'

def writeToFile(data, filename):
	f = open(filename, 'w')
	f.write(data)
	f.close()

def getInstagramLinkLike(media_id):
	
	return 'https://www.instagram.com/web/likes/' + media_id + '/like/'

def instagramAuthorisation(br, nm):
		url = 'https://api.instagram.com/oauth/authorize/'

		data = {
			'client_id' : str(profile['CREDENTIALS' + str(nm)]['CLIENT_ID' + str(nm)]),
			'redirect_uri' : str(profile['CREDENTIALS' + str(nm)]['REDIRECT_URL' + str(nm)]),
			'response_type' : 'code'
		}
		r = requests.get(url, params=data)

		br.open(r.url)

		username = str(profile['INSTAGRAM' + str(nm)]['USERNAME' + str(nm)])
		print('User: %s\n' % username)

		br.select_form(nr=0)
		br['username'] = username
		br['password'] = str(profile['INSTAGRAM' + str(nm)]['PASSWORD' + str(nm)])
		br.submit()

		# time.sleep(5)

		print('Instagram: you have been successfully authorized.\n')

# Function to parse the Top HashTag page and get the current top hashtags
def getTopHashTags(br):
		 br.open('http://top-hashtags.com/instagram/1/')
		 # <a href="/tag/
		 topHashtags = re.findall('[a-z]+\/\"\>\#[a-z]+', br.response().read())
		 
		 length = profile['MAX_HASHTAGS'] if profile['MAX_HASHTAGS'] < len(topHashtags) else len(topHashtags)

		 print('\nMax hashtags: %s' % length)

		 hashtags = []

		 for i in range(length):
		 	hashtags.append(topHashtags[i].split('#')[1])

		 return hashtags
		 
# Function to read the hashtags from a users file if not wanting to parse the top 100
def getHashtagsFromFile():
	 #your list of hashtags
	 hashtags = []
	 filename = 'hashtags.txt'
	 #Hashtag file input
	 f = open(filename)
	 #strips newline character
	 hashtags = [unicode(line.strip(), 'utf-8') for line in open(filename)]
	 f.close()
	 return hashtags

def getCookies(br):
	cookiesjar = br._ua_handlers['_cookies'].cookiejar

	cookies = {}

	for cookie in cookiesjar:
		cookies[cookie.name] = cookie.value

	return cookies

def getHeaders(csrftoken):
	return {'accept' : '*/*', 
	'accept-encoding' : 'gzip, deflate, br',
	'accept-language' : 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
	'content-length' : '0',
	'content-type' : 'application/x-www-form-urlencoded',
	'origin' : 'https://www.instagram.com',
	'referer' : 'https://www.instagram.com/pogorelov.maxim/',
	'x-csrftoken' : csrftoken,
	'user-agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
	'x-instagram-ajax' : '1',
	'x-requested-with' : 'XMLHttpRequest'}

def sendLike(link, cookie, headers, br):
	# print('Cookies: %s\n\n' % cookie)
	
	result = False

	# print('Headers: %s\n\n' % headers)
	try:
		r = requests.post(link, cookies=cookie, headers=headers)
	except Exception: 
		return result	

	if r.status_code == 200:
		result = True
	else:
		print('Status: Failed! Code: %s' % str(r.status_code))

	return result
	 
# Function to like hashtages
def like(br, hashtags, nm):
	maxLikesPerTags = profile['PER_HASHTAG']
	global likes

	 
	print('\nMax likes per tag: %d \n' % maxLikesPerTags)


	for hashtag in hashtags:

		isFailed = False

		print('\nCurrent hashtag: %s \n' % hashtag)


		link = INSTAGRAM_TAG_URL + hashtag
	 
	 	try:
			r = requests.get(link)
		except Exception: 
			print('\nUnable to open link for %s hashtag!\n' % hashtag)
			continue	

	 	if r.status_code == 404:
	 		print('\nPage not found for %s hashtag!\n' % hashtag)
	 		continue

	 	jsonResult = json.loads(re.findall('(window\.\_sharedData\s=\s\{.+};\<\/script>)', r.text.encode('utf-8'))[0][21:-10])

	 	# writeToFile(json.dumps(jsonResult, indent=4, sort_keys=True), 'logpage.html')

	 	medias = jsonResult['entry_data']['TagPage'][0]['tag']['media']['nodes']
	 	
	 	for i in range(len(medias)):
	 		media_id = medias[i]['id'].encode('ascii','ignore')
	
	 		if i == maxLikesPerTags:
				print('\nStop liking \'%s\' hashtag!' % hashtag)
				break

			cookies = getCookies(br)
			headers = getHeaders(cookies['csrftoken'])
			link = getInstagramLinkLike(media_id)
			
			isLiked = sendLike(link, cookies, headers, br)

			if isLiked:
				likes += 1
				print('[%s] Liked: %d' % (str(profile['INSTAGRAM' + str(nm)]['USERNAME' + str(nm)]),likes))
				time.sleep(profile['SLEEPTIME'])

	print('Done!')
			
def printTitle():
	print("|=================================|")
	print("|       InstaPromoter v2.0        |")
	print("|  Developed by Maxim Pogorelov   |")
	print("|=================================|\n\n")
	print("")


def runner(times, nm):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_handle_equiv(False)
	br.addheaders = [('User-Agent', USER_AGENT), ('Accept', '*/*')]
	# nm = 1

	instagramAuthorisation(br, nm)
		 
	if profile['HOT_HASHTAGS']:
		  hashtags = getTopHashTags(br)
	else:
		  hashtags = getHashtagsFromFile()

	print("\nHashtags found: %s" % hashtags)

	for i in range(times):
		like(br, hashtags, nm)


if __name__ == "__main__":
	printTitle()
	with open("InstaPromoterProfile.yml", "r") as f:
		profile = yaml.safe_load(f) 

	likes = 0

	nm = str(sys.argv[1])

	repeat_times = profile['REPEAT_TIMES']
	perHashtag = profile['PER_HASHTAG']
	maxHashtags = profile['MAX_HASHTAGS']

	resultedLikes = repeat_times * perHashtag * maxHashtags

	sleeptime = profile['SLEEPTIME']
	sec = sleeptime * resultedLikes
	dateTake = str(datetime.timedelta(seconds = sec))

	print("Liked posts should be less or equal to %d and it will take around %s \n\n" % (resultedLikes, dateTake))

	runner(repeat_times, nm)