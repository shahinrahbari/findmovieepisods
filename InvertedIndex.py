from stemming.porter2 import stem

import unicodedata

import fileinput

from glob import glob

from collections import Counter

from math import log

from collections import Counter


import json 
import requests

import time


TOKEN = "302605615:AAHDIdXEnEg3OYt_g2wDsAGY8w4v7ZCDFj0"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


# _STOP_WORDS = frozenset([
# 'a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again', 
# 'against', 'all', 'almost', 'alone', 'along', 'already', 'also','although',
# 'always','am','among', 'amongst', 'amoungst', 'amount',  'an', 'and', 'another',
# 'any','anyhow','anyone','anything','anyway', 'anywhere', 'are', 'around', 'as',
# 'at', 'back','be','became', 'because','become','becomes', 'becoming', 'been', 
# 'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 
# 'between', 'beyond', 'bill', 'both', 'bottom','but', 'by', 'call', 'can', 
# 'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe', 
# 'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 
# 'either', 'eleven','else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 
# 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 
# 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 
# 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get',
# 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 
# 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 
# 'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc', 
# 'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 
# 'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 
# 'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 
# 'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never', 
# 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 
# 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only',
# 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
# 'over', 'own','part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
# 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 
# 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 
# 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 
# 'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their', 
# 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 
# 'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third',
# 'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 
# 'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 
# 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 
# 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',
# 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 
# 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 
# 'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
# 'yourselves', 'the'])

_STOP_WORDS = frozenset([])

def words_split(text):
    
    List_of_words = []
    current_word = []
    current_index = None

    for i, c in enumerate(text):
        if c.isalnum():
            current_word.append(c)
            current_index = i
        elif current_word:
            word = u''.join(current_word)
            List_of_words.append((current_index - len(word) + 1, word))
            current_word = []

    if current_word:
        word = u''.join(current_word)
        List_of_words.append((current_index - len(word) + 1, word))

    return List_of_words

def remove_stopwords(words):
    
    New_list_of_words = []
    for index, word in words:
        if word in _STOP_WORDS:
            continue
        else :
            New_list_of_words.append((index, word))
    return New_list_of_words

def lowercase(words):

    lowercase_words = []
    for index, word in words:
        words_lower = word.lower()
        lowercase_words.append((index, words_lower))
    return lowercase_words

def porterstemmer(words):
    
    ported_words = []
    for index, word in words:
        stemming_word = stem(word)
        ported_words.append((index, stemming_word))
    return ported_words
        

def normalize_words(text):

    words = words_split(text)
    words = remove_stopwords(words)
    words = lowercase(words)
    words = porterstemmer(words)
    return words

def inverted_index(text):
    """
        {word:[locations]}
    """
    inverted = {}
 

    for index, word in normalize_words(text):
        locations = inverted.setdefault(word, [])
        locations.append(index)
        

    return inverted

def inverted_index_positional(inverted, document_id, document_index):
    """
        {word:{document_id:[locations]}}
    """
    for word, locations in document_index.iteritems():
        location_with_document_id = inverted.setdefault(word, {})
        location_with_document_id[document_id] = locations
    
    return inverted



def write_Inverted_Index_To_File(inverted):
    
    f=open("./indexFile", 'w')
    for word in inverted.iterkeys():
        postinglist=[]
        for p, q in inverted[word].iteritems():
            docID=p
            positions=q
            postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
        print >> f, ''.join((word,'|',';'.join(postinglist)))

    f.close()


def readInvertedIndex():
    inverted = {}
    f=open("./indexFile", 'r');
    for line in f:
        line=line.rstrip()
        word, postings = line.split('|')    
        postings=postings.split(';')        
        postings=[x.split(':') for x in postings] 
        postings=[ [int(x[0]), map(int, x[1].split(','))] for x in postings ]   
        inverted.setdefault(word,[])
        inverted.append(postings)
    f.close()
    return inverted


def return_term_frequency(word,docid,inverted):
    if word in inverted.iterkeys():
        if docid in inverted[word].iterkeys():
            return len(inverted[word][docid])
        else:
            return None
    else:
        return None

def return_document_frequency(word,docid,inverted):
    if word in inverted.iterkeys():
        if docid in inverted[word].iterkeys():
            return len(inverted[word][docid])
        else:
            return None
    else:
        return None

def return_weight_of_term(word,docid,inverted,N):
    tf = return_term_frequency(word,docid,inverted)
    df = return_document_frequency(word,docid,inverted)
    W =  tf * log(N/df)
    return W



def return_length_of_document(docid):
    list_of_words = words_split(docid)
    return len(list_of_words)


def return_average_of_documents_lengths(listed_documents):
    list_of_document_lengths = []
    for document in listed_documents:
        l = return_length_of_document(document)
        list_of_document_lengths.append(l)
    return (sum(list_of_document_lengths))/len(listed_documents)



def rank(query,docid,inverted,avg_l,N):
    b=0.75 
    k1=1.2
    score = 0
    l = return_length_of_document(docid)
    for word in query:
        tf = return_term_frequency(word,docid,inverted)
        df = return_document_frequency(word,docid,inverted)
        print 'n: ',N
        print 'df: ',df
        if df != None:
            idf = log((N - df + 0.5) / (df + 0.5))
            score += (idf * (tf * (k + 1)) / (tf + k * (1 - b + (b * l / avg_l))))

    return score



def n_gram(text):
    
    print 'this is for n_gram inverted index !'
    n = input('plz input n: ')
    list_of_grams = []
    current_gram = []
    i = 0
    for c in text:
        if c.isalnum():
            current_gram.append(c)
            i = i +1
            if (i == n):
                list_of_grams.append(current_gram)
                current_gram = []
                i = 0
    print list_of_grams

    
def search(inverted, query):

    words = []
    results = []
    final_result = []
    list_of_tfs = []
    list_of_documents = []
    tfs = {}
    
    for _, word in normalize_words(query):
        if word in inverted :
            words.append(word)
    for word in words:
        results.append(inverted[word].keys())

    
            
    if results:

        reduce(lambda x, y: x & y, results)
        
        for word in words:
            for _, document_locations in inverted[word].iteritems():
                x = len(document_locations)
                list_of_tfs.append(x)
                             
        for document in results:
            for doc_id in document:
                list_of_documents.append(doc_id)
                
        tfs = dict(zip(list_of_documents,list_of_tfs))
        sorted_tfs = Counter(tfs)

        
        #return sorted_tfs.most_common()
        return list_of_documents
    
    
def final_search_result(list):
    final_result = []
    for r in list:
        final_result.append(r)
    final_result = intersectLists(final_result)

    return final_result

def permute_index(inverted):
    permute_dic = {}
    
    for word in inverted.iterkeys():
        new_word = word + '$'
        permute_dic[new_word] = word
        while new_word[0] != '$':
            new_word = new_word[1:] + new_word[0]
            permute_dic[new_word] = word
    
    return permute_dic


def write_Permute_Index_To_File(pindex):
    
    f=open("./pindex", 'w')
    for word in pindex.iterkeys():
        print >> f, ''.join((word,'|',pindex[word]))
    f.close()



def intersectLists(lists):
    if len(lists) == 0:
        return []
    lists.sort(key=len)
    return list(reduce(lambda x,y: set(x) & set(y), lists))


def WildCard_search(inverted,permute_dic,queries):
    queries = queries.lower()
    queries = queries.split()
    result = []
    list_of_words = []
    for query in queries:
        query_result = []
        splited_query = query.split('*')
        new_query = splited_query[1] + '$' + splited_query[0]
        
        for word in permute_dic.iterkeys():
            
            word_result = []
            if word[:len(new_query)] == new_query:
                
                for k,v in inverted[permute_dic[word]].iteritems():
                    
                    try:
                        word_result.append(k)
                        list_of_words.append(permute_dic[word])
                    except:
                        word_result = [k]
                    
            try:
                query_result.extend(word_result)
            except:
                query_result = word_result
        if result == []:
            result = [query_result]
        else:
            result.append(query_result)

    if result == []:
        print 'none'
    else :
        reduce(lambda x, y: x & y, result)
        result = intersectLists(result)
        result.sort()

    new_result = dict(zip(result,list_of_words))
    return new_result





def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)




def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)



if __name__ == '__main__':



    inverted = {}
    s = 47
    documents = {}
    for i in range(1, s+1):
        i = str(i)
        with open('doc' + i + '.txt') as f:
            documents['doc' + i] = f.read()


    for document_id, text in documents.iteritems():
        document_index = inverted_index(text)
        inverted_index_positional(inverted, document_id, document_index)

    
    write_Inverted_Index_To_File(inverted)


    for word, document_locations in inverted.iteritems():
        print word, document_locations,
        print '\n',
        for k,v in document_locations.iteritems():
            print 'tf in ',k,'is: ',len(v)
        print '___________________________________'

    






    last_textchat = (None, None)
    while True:



        text, chat = get_last_chat_id_and_text(get_updates())

        if (text, chat) != last_textchat:

            n = text
            queries = n.split(' ')
            list_for_final_result = []
            all_results = []

            for query in queries:
                if '*' in query:

                    p_Dic = permute_index(inverted)
                    write_Permute_Index_To_File(p_Dic)
                    result = WildCard_search(inverted,p_Dic,query)
                else:
                    result = search(inverted, query)
                    if result:

                        if (len(result) > 0):
                            for r in result:
                                list_for_final_result.append(r)
                        all_results.append(result)

            final_final_result = []
            
            if(not all_results):
                send_message("No Episode found! :(",chat)

            fresult = set(all_results[0])
            for s in all_results[1:]:
                fresult.intersection_update(s)
            print "len: ",len(fresult) 

            fresult = list(fresult)

            if (int(fresult[0][-2:]) < 25):
                #print "Friends Season 1 " + "Episode " + fresult[0][-2:]
                send_message("Friends Season 1 " + "Episode " + fresult[0][-2:],chat)
            elif(int(fresult[0][-2:]) >= 25 and int(fresult[0][-2:]) <=36):
                #print "Friends Season 2 " + "Episode " + str(int(fresult[0][-2:])-24)
                 send_message("Friends Season 2 " + "Episode " + str(int(fresult[0][-2:])-24),chat)
            else:
                #print "Friends Season 2 " + "Episode " + str(int(fresult[0][-2:])-23)
                send_message("Friends Season 2 " + "Episode " + str(int(fresult[0][-2:])-23),chat)

            if (text, chat) != last_textchat:
                #send_message(text, chat)
                last_textchat = (text, chat)
        time.sleep(0.5)






 
                
   

        

    
