import nltk, pickle, matplotlib.pyplot as plt
#import streamlit as st,
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = nltk.WordNetLemmatizer()

#st.title('Concordia Discourse: The Concordiensis Analyzer')

search_terms = input("Please enter a search term(s): ")
search_terms = search_terms.split()
search_terms = [term.lower() for term in search_terms if term.isalpha()]

lem_ans = input("Lemmatize? y/n: ")
lem_ans = lem_ans.lower()
if lem_ans == "y":
    search_terms = [lemmatizer.lemmatize(term) for term in search_terms]
    pickleIn = open("concordy_dictionary_lemma_pickle.pickle",'rb')
else:
    pickleIn = open("concordy_dictionary_raw_pickle.pickle",'rb')

# if search_terms.isalpha():
#     search_terms = search_terms.lower()

# search_term = st.text_input("Please enter a search term: ")
# if search_term.isalpha():
#   search_term = search_term.lower()

concordy_dictionary = pickle.load(pickleIn)

start_year = 1880
end_year = 2000
years = range(start_year,end_year+1)

list_of_clean_toks_for_each_year_list = list()
norm_term_counts = list()

dict_search_terms_counts = {term : [] for term in search_terms}

for year in years:
    list_of_clean_words_year = list()
    for k,v in concordy_dictionary.items():
        if k[:4] == str(year):
            for tok in v:
                list_of_clean_words_year.append(tok)
    list_of_clean_toks_for_each_year_list.append(list_of_clean_words_year)

for year_toks_list in list_of_clean_toks_for_each_year_list:
    year_word_count = len(year_toks_list)
    for key_search_term,val_term_counts_list in dict_search_terms_counts.items():
        search_term_count = year_toks_list.count(key_search_term)
        try:
            norm_count = (search_term_count/year_word_count)*1000000
        except:
            val_term_counts_list.append(0) 
        else:
            val_term_counts_list.append(norm_count)

Figure = plt.figure(figsize = (12, 8))
for key_term,val_norm_counts_list in dict_search_terms_counts.items():
    plt.plot(years,val_norm_counts_list,label=key_term, figure=Figure)
    plt.title("Term Frequency in the Concordiensis, 1880-2000")
    plt.xlabel('year')
    plt.ylabel('words per million')
    plt.legend()
plt.show()


#st.pyplot()

# search_term_count = 0
# for year_text in list_of_clean_words_for_each_year:
#     year_word_count = len(year_text)
#     for key_search_term,val_term_list in dict_search_terms_counts.items():
#         search_term_count = sum(1 if re.fullmatch(key_search_term,token) else 0 for token in year_text)
#         try:
#             norm_count = (search_term_count/year_word_count)*1000000
#         except:
#             val_term_list.append(0)
#         else:
#             val_term_list.append(norm_count)
#         #         sum(1)
#         #     else:
#         #         sum(0)
#         # search_term_count = 
#         # search_term_count = year_text.count(key_search_term)