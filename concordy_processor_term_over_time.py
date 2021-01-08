import nltk, pickle, matplotlib.pyplot as plt, streamlit as st, numpy as np
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = nltk.WordNetLemmatizer()

st.title("DigiCordy: The Union College Concordiensis Analyzer")

st.sidebar.image("UC_logo_with_date.PMS202.png", width=200)
#enter search terms
# search_terms = input("Please enter your search term(s). If entering multiple search terms, please divide them with a space: ")
# search_terms = search_terms.split()
search_terms = st.sidebar.text_input("Please enter your search term(s). If entering multiple search terms, please divide them with a space: ")
search_terms = search_terms.split()

#set year range / timeline
# start_year = 1880
# end_year = 2000
start_year = st.sidebar.slider(label="Please choose a start year.", min_value=1880, max_value=1999,step=1)
end_year = st.sidebar.slider(label="Please choose an end year.", min_value=1881, max_value=2000,step=1)
years = range(start_year,end_year+1)

# lem_ans = input("Lemmatize the data? y/n: ")
# if lem_ans == "y":
#     pickleIn = open("concordy_lemma.pickle",'rb')
#     d_year_month_text = pickle.load(pickleIn)
#     search_terms = [lemmatizer.lemmatize(term.lower()) for term in search_terms if term.isalpha()]

# else:
#     pickleIn = open("concordy_raw_no_POS.pickle",'rb')
#     d_year_month_text = pickle.load(pickleIn)
#     case_ans = input("Lower case the data? y/n: ")
#     if case_ans == "y":
#         search_terms = [term.lower() for term in search_terms if term.isalpha()]
#         for year in years:
#             for month in d_year_month_text[year].keys():
#                 d_year_month_text[year][month] = [word.lower() for word in d_year_month_text[year][month]]


lem_ans = st.sidebar.selectbox(label="Lemmatize the data?", options=("Yes","No"), index=0)
if lem_ans == "Yes":
    pickleIn = open("concordy_lemma.pickle",'rb')
    d_year_month_text = pickle.load(pickleIn)
    search_terms = [lemmatizer.lemmatize(term.lower()) for term in search_terms if term.isalpha()]
else:
    pickleIn = open("concordy_raw_no_POS.pickle",'rb')
    d_year_month_text = pickle.load(pickleIn)
    case_ans = st.sidebar.selectbox(label="Lower case the data?", options=("Yes","No"), index=0)
    if case_ans == "Yes":
        search_terms = [term.lower() for term in search_terms if term.isalpha()]
        for year in years:
            for month in d_year_month_text[year].keys():
                d_year_month_text[year][month] = [word.lower() for word in d_year_month_text[year][month]]

#Create list of year words
for year in years:
    list_of_words_year = [tok for list_of_issue_words in d_year_month_text[year].values() for tok in list_of_issue_words]
    d_year_month_text[year] = list_of_words_year

#get count of words for each year and get count of appearances of search term in words for each year, norm counts, 
# and add normed counts to (dict-value: empty list of counts) associated with (dict-key: search term)
dict_search_terms_counts = {term : [] for term in search_terms}
for year in years:
    year_words_list = d_year_month_text[year]
    year_word_count = len(year_words_list)
    for key_search_term,val_term_counts_list in dict_search_terms_counts.items():
        search_term_count = year_words_list.count(key_search_term)
        try:
            norm_count = (search_term_count/year_word_count)*1000000
        except:
            val_term_counts_list.append(0) 
        else:
            val_term_counts_list.append(norm_count)

#visualize chart
#Figure = plt.figure(figsize = (12, 8))
fig,ax = plt.subplots(figsize = (15, 10))
for key_term,val_norm_counts_list in dict_search_terms_counts.items():
    ax.plot(years,val_norm_counts_list,label=key_term)
ax.set_title("Term Frequency in the Concordiensis, 1880-2000")
ax.set_xlabel('year')
ax.set_ylabel('words per million')
ax.legend()
plt.xticks(np.arange(min(years), max(years)+1, 10))
st.pyplot(fig)
#plt.show()

st.text("DigiCordy is a collaborative project of Adam Mazel (Digital Scholarship and Instruction Librarian), Nick Webb (Professor of Computer Science), Schaffer Library, and the Center for Data Analytics.")


#Remove Punctuation from (tok,tag)
# for year in years:
#     for month in d_year_month_text[year].keys():
#         d_year_month_text[year][month] = [tuple_tok_tag for tuple_tok_tag in d_year_month_text[year][month] if tuple_tok_tag[0].isalnum()]

# #Lemmatize option code goes here


# #Remove tags from (tok,tag)
# for year in years:
#     for month in d_year_month_text[year].keys():
#         d_year_month_text[year][month] = [tuple_tok_tag[0] for tuple_tok_tag in d_year_month_text[year][month]]




# list_of_ready_toks_for_each_year_list = list()
# for year in years:
#     for month in d_year_month_text[year].keys():
#         list_of_lemma_tags_issue = list()
#         for tuple_tok_tag in d_year_month_text[year][month]:
#             if tuple_tok_tag[1].startswith("N"):
#                 lemmatizer.lemmatize(tuple_tok_tag[0], pos="n")
#                 list_of_lemma_tags_issue.append(tuple_tok_tag)
#             elif tuple_tok_tag[1].startswith("V"):
#                 list_of_lemma_tags_issue.append(lemmatizer.lemmatize(tuple_tok_tag[0], pos="v"))
#             elif tuple_tok_tag[1].startswith("J"):
#                 llist_of_lemma_tags_issue.append(lemmatizer.lemmatize(tuple_tok_tag[0], pos="a"))
#             else:
#                 list_of_lemma_tags_issue.append(lemmatizer.lemmatize(tuple_tok_tag[0]))
#         d_year_month_text[year][month] = 

# #     for year in years:
# #         list_of_processed_words_year = list()
# #         for list_of_issue_tups_of_tok_tag in d_year_month_text[year].values():
# #             for tups_of_tok_tag in list_of_issue_tups_of_tok_tag:
                # if tups_of_tok_tag[1].startswith("N"):
                #     lemmatizer.lemmatize(tups_of_tok_tag[0], pos="n")
                # elif tups_of_tok_tag[1].startswith("V"):
                #     lemmatizer.lemmatize(tups_of_tok_tag[0], pos="v")
                # elif tups_of_tok_tag[1].startswith("J"):
                #     lemmatizer.lemmatize(tups_of_tok_tag[0], pos="a")
                # else:
                #     lemmatizer.lemmatize(tups_of_tok_tag[0])
# #                 list_of_processed_words_year.append(tups_of_tok_tag[0].lower())



# # lem_ans = input("Lemmatize text? y/n: ")
# # lem_ans = lem_ans.lower()

# # case_ans = input("Lowercase text? y/n: ")
# # case_ans = case_ans.lower()

# # lem_case_ans = lem_ans+case_ans




# # if lem_case_ans == "yy":
# #     search_terms = [lemmatizer.lemmatize(term) for term in search_terms]
# #     for year in years:
# #         list_of_processed_words_year = list()
# #         for list_of_issue_tups_of_tok_tag in d_year_month_text[year].values():
# #             for tups_of_tok_tag in list_of_issue_tups_of_tok_tag:
# #                 if tups_of_tok_tag[1].startswith("N"):
# #                     lemmatizer.lemmatize(tups_of_tok_tag[0], pos="n")
# #                 elif tups_of_tok_tag[1].startswith("V"):
# #                     lemmatizer.lemmatize(tups_of_tok_tag[0], pos="v")
# #                 elif tups_of_tok_tag[1].startswith("J"):
# #                     lemmatizer.lemmatize(tups_of_tok_tag[0], pos="a")
# #                 else:
# #                     lemmatizer.lemmatize(tups_of_tok_tag[0])
# #                 list_of_processed_words_year.append(tups_of_tok_tag[0].lower())
# #         list_of_ready_toks_for_each_year_list.append(list_of_processed_words_year)

# # elif lem_case_ans == "nn":
# #     for year in years:
# #         list_of_processed_words_year = list()
# #         for list_of_issue_tups_of_tok_tag in d_year_month_text[year].values():
# #             for tups_of_tok_tag in list_of_issue_tups_of_tok_tag:
#                 list_of_processed_words_year.append(tups_of_tok_tag[0])
#         list_of_ready_toks_for_each_year_list.append(list_of_processed_words_year)

# elif lem_case_ans == "yn":
#     search_terms = [lemmatizer.lemmatize(term) for term in search_terms]
#     for year in years:
#         list_of_processed_words_year = list()
#         for list_of_issue_tups_of_tok_tag in d_year_month_text[year].values():
#             for tups_of_tok_tag in list_of_issue_tups_of_tok_tag:
#                 if tups_of_tok_tag[1].startswith("N"):
#                     lemmatizer.lemmatize(tups_of_tok_tag[0], pos="n")
#                 elif tups_of_tok_tag[1].startswith("V"):
#                     lemmatizer.lemmatize(tups_of_tok_tag[0], pos="v")
#                 elif tups_of_tok_tag[1].startswith("J"):
#                     lemmatizer.lemmatize(tups_of_tok_tag[0], pos="a")
#                 else:
#                     lemmatizer.lemmatize(tups_of_tok_tag[0])
#                 list_of_processed_words_year.append(tups_of_tok_tag[0])
#         list_of_ready_toks_for_each_year_list.append(list_of_processed_words_year)

# elif lem_case_ans == "ny":
#     for year in years:
#         list_of_processed_words_year = list()
#         for list_of_issue_tups_of_tok_tag in d_year_month_text[year].values():
#             for tups_of_tok_tag in list_of_issue_tups_of_tok_tag:
#                 list_of_processed_words_year.append(tups_of_tok_tag[0].lower())
#         list_of_ready_toks_for_each_year_list.append(list_of_processed_words_year)
