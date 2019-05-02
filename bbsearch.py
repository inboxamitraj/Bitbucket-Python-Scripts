"""
# Author - Amit Raj
# Description- search a string in all the bitbucket repos
# This is using elastic search Rest APIs to search the string
# auth_string can be encoded from https://www.base64decode.org/
# History: 02-05-2019 public version
"""
import json
import urllib3

urllib3.disable_warnings()

bb_url_el = "http://domainname:port"  # elastic search URL e.g. http://localhost:9200
bb_url = "https://domainname:port/contextpath"  # bitbucket url e.g. https://bitbucketcompany:443/git
auth_string_el = "***"  # elastic search username:password in bas64 encoded
auth_string_bb = "***"  # bitbucket username:password in bas64 encoded

input_string_file = "C:/Users/username/Desktop/input_string.txt"  # strings to search, you can give mulitple strings in newline in the input file
open_input_file = open(str(input_string_file))
open_input_list = open_input_file.read().split("\n")  # create a list from the file
open_input_file.close()


# Everything indexed in bitbucket is under bitbucket-search-v1 index
def get_result(bb_url_el, search_string, size_index, from_index):
    URL = str(bb_url_el) + "/bitbucket-search-v1/_search?size=" + str(size_index) + "&from=" + str(
        from_index) + "&q=" + str(search_string)
    print("URL: ", URL)
    http = urllib3.PoolManager()
    header = {'Content-Type': 'application/json', 'Authorization': 'Basic ' + str(auth_string_el)}
    req = http.request('GET', URL, headers=header)
    resp = json.loads(req.data.decode('utf-8'))
    return resp


for search_string in open_input_list:
    result = get_result(bb_url_el, search_string, 1000, 0)
    match_count = result['hits']['total']
    length = len(result['hits']['hits'])
    print("searching string: ", search_string)
    print("total matches: ", match_count)
    i = 0
    print("Index", ",", "ProjectID", ",", "RepoId", ",", "Path")
    while length > i:
        print(i, ",", result['hits']['hits'][i]['_source']['projectId'], ",",
              result['hits']['hits'][i]['_source']['repositoryId'],
              ",", result['hits']['hits'][i]['_source']['path'])
        i += 1
