import time 
import requests
import os
import sys

# Import library to display results
_url = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/analyze'
_key = 'e603af62bcca48f5ac497802bbae3a44'  #Here you have to paste your primary key
_maxNumRetries = 10
thumb_size = 512

if len(sys.argv) > 1:
	mypics = [sys.argv[1]]
else:
	mypics = [os.getcwd() + '/' + i for i in os.listdir(os.getcwd()) if i[-4:]=="jpeg" or i[-3:] in ('png','jpg','gif','bmp')]

def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json()['error']['message'] ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )
            print( "Check internet connection, or API limit (20 images/min) exceeded" )

        break
        
    return result


for imgurl in mypics:
	# Load raw image file into memory
	pathToTempFolder = os.environ["TMPDIR"] + 'hacktech/'
	print("Downsampling photo with Quick Look...")
	os.system('qlmanage -t \'%s\' -s '%(imgurl) + str(thumb_size) + ' -o ' + pathToTempFolder)
	pathToThumb = pathToTempFolder + imgurl.split('/')[-1] + '.png'
	print("Sending API Request... Close terminal window to exit.")
	with open( pathToThumb, 'rb' ) as f:
	    data = f.read()
	    
	# Computer Vision parameters
	params = { 'visualFeatures' : 'Tags'} 

	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _key
	headers['Content-Type'] = 'application/octet-stream'

	json = None

	result = processRequest( json, data, headers, params )
	print("Tags for %s: "%(imgurl.split('/')[-1]) + str([i['name'] for i in result['tags'] if i['confidence'] > 0.5]))

	for r in [i['name'] for i in result['tags'] if i['confidence'] > 0.5]:
		os.system('tag --add \'%s\' \'%s\'' % (r, imgurl))


