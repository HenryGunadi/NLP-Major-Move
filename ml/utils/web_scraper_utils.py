# def extract_tokens(name):
#     # Remove common suffix like "Tbk", "PT", etc.
#     name = re.sub(r'\b(Tbk|PT|Tbk\.|Tbk,?)\b', '', name, flags=re.IGNORECASE)
#     return [token.strip().lower() for token in name.split() if len(token) > 2]  # Exclude short irrelevant words

# company_tokens_list = stock_list_df["Company Name"].apply(extract_tokens).explode().unique().tolist()

# url = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069"
# feed = feedparser.parse(url)

# print(len(feed.entries))

# for key, value in feed.entries[20].items():
#   print(f"{key} : {value}")

# import re

# related_data = []

# def checkRelatedCompanies(value):
#     matched_codes = stock_list_df["Code"].loc[
#         stock_list_df["Code"].apply(lambda data: bool(re.search(rf'\b{re.escape(data)}\b', value)))
#     ].tolist()
    
#     matched_companies = [
#         name for name in stock_list_df["Company Name"].tolist() 
#         if name.lower() in value.lower()
#     ]
    
#     return matched_codes, matched_companies

# def clean_html(raw_html):
#     """Remove HTML tags from a string."""
#     return re.sub(r'<.*?>', '', raw_html).strip()

# for entry in feed.entries:
#     matched_codes = []
#     matched_companies = []
#     contents = []

#     summary = entry["summary"]
#     title = entry["title"]
#     summary_detail = entry["summary_detail"]["value"]

#     # Search through title, summary, and summary_detail
#     for text in [title, summary, summary_detail]:
#         codes, companies = checkRelatedCompanies(text)
#         matched_codes += codes
#         matched_companies += companies

#     # Look inside content (usually body HTML)
#     for content in entry.get("content", []):
#         if content["type"] == "text/html":
#             content_value = clean_html(content["value"])
#             codes, companies = checkRelatedCompanies(content_value)
#             if codes or companies:
#                 matched_codes += codes
#                 matched_companies += companies
#                 contents.append(content_value)

#     # Skip if the article doesn't mention any related code/company
#     if not matched_codes and not matched_companies:
#         print("The article is not stock related.")
#         continue

#     # Store only unique values
#     related_data.append({
#         "link": entry["id"],
#         "date_published": entry["published"],
#         "title": title,
#         "summary": summary,
#         "matched_codes": list(set(matched_codes)),
#         "matched_companies": list(set(matched_companies)),
#         "contents": contents,
#     })


# for index, data in enumerate(related_data):
#   print(f"Index {index} : ")
  
#   for key, value in data.items():
#     print(f"{key} : {value}")
  
#   print()

