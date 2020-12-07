import ssl, urllib, nltk, pickle
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = nltk.WordNetLemmatizer()

ssl._create_default_https_context = ssl._create_unverified_context

URLfolder = "https://cs-gitlab.union.edu/webbn/concordy/raw/master/Text/"

start_year = 1880
end_year = 2000
years = range(start_year,end_year+1)

d_year_month_text = dict()

for year in years:
  print(year)

  for month in range(1,13):
    monthStr = str(month)
    if month < 10:
      monthStr = "0"+monthStr

    path = URLfolder+str(year)+"-"+monthStr+".txt"
    req = urllib.request.Request(path)
  
    try:
      urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
      print(monthStr,'MISSING: Error code: ', e.code)
    except urllib.error.URLError as e:
      print('Reason: ', e.reason)
    else:
      response = urllib.request.urlopen(path)
      data = response.read()      
      text = data.decode('utf-8') 
      tokens = nltk.word_tokenize(text)
      clean_words = [token.lower() for token in tokens if token.isalnum()]
      lemma_words = [lemmatizer.lemmatize(word) for word in clean_words]
      d_year_month_text[str(year)+"_"+monthStr] = lemma_words

pickleOut = open('concordy_dictionary_lemma_pickle.pickle','wb')
pickle.dump(d_year_month_text,pickleOut)
pickleOut.close()