# Product Matching Between Ecommerce Sites using Cosine Similarity

**Introduction:**

In this project, we aim to match products between two popular ecommerce sites, namely Amazon and Flipkart. We employ various techniques such as web scraping, cosine similarity, and the use of sentence transformers to accomplish this task. The project is implemented using Flask, a lightweight web framework for Python.

### Table of Contents

1. Introduction
2. Data Collection and Preprocessing
3. Cosine Similarity
4. Sentence Transformers
5. Implementation with Flask
6. Conclusion
7. References

![image](https://github.com/PankajBarai/productMatching/assets/96985326/2de2ace5-0922-4bf7-9179-bf6c749c6b6d)


**1. Introduction:**

Ecommerce sites have a vast collection of products, making it challenging for users to find the same product across different platforms. Our goal is to create a system that can match products between Amazon and Flipkart based on their textual descriptions. By leveraging advanced techniques such as cosine similarity and sentence transformers, we can effectively find similar products.

**2. Data Collection and Preprocessing:**

To gather product information from Amazon and Flipkart, we utilize Beautiful Soup, a Python library for web scraping. We extract relevant details such as product names, descriptions, and other attributes. The scraped data is then preprocessed to remove any unnecessary characters, convert text to lowercase, and handle punctuation.

**3. Cosine Similarity:**

Cosine similarity is a measure used to determine the similarity between two vectors. In our case, we represent product descriptions as vectors, where each word is a dimension. By calculating the cosine similarity between two product vectors, we can quantify their textual similarity. We employ the cosine similarity implementation provided by scikit-learn, a popular machine learning library.

**4. Sentence Transformers:**

Sentence transformers are pre-trained models that encode sentences into dense vector representations, capturing their semantic meaning. By utilizing sentence transformers, we can obtain high-quality representations of product descriptions. These embeddings enable us to measure the semantic similarity between different product descriptions effectively.

**5. Implementation with Flask:**

Our implementation uses Flask, a web framework, to create a user-friendly interface. Users can enter a query representing a product of interest. The system then searches for similar products across Amazon and Flipkart by computing the cosine similarity between the query and the product descriptions. The top 10 matching products from both sites are displayed to the user.

**6. Conclusion:**

In this project, we have demonstrated the application of cosine similarity and sentence transformers to match products between ecommerce sites. By leveraging these techniques, we can provide users with a convenient way to find similar products across different platforms. The Flask implementation allows for easy deployment and user interaction.

**7. References:**

- Sentence Transformers: [https://www.sbert.net/](https://www.sbert.net/)
- Cosine Similarity (scikit-learn): [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
- Beautiful Soup: [https://www.crummy.com/software/BeautifulSoup/](https://www.crummy.com/software/BeautifulSoup/)
- Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- NumPy: [https://numpy.org/](https://numpy.org/)
- Pandas: [https://pandas.pydata.org/](https://pandas.pydata.org/)

Please note that the links provided are subject to change as new versions of the libraries or frameworks are released. It's always a good practice to refer to the official documentation for the most up-to-date information.
