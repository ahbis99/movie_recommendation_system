# Movie Recommender System
This is our project which we finished in 24 hours for Dragon Hackathon in University of Ljubljana.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Visualizations from project](#visualizations-from-project)

## General info

This project aims to simplify the process of choosing movies for viewers. Making a decision on which movie to watch can often be time-consuming, so our project streamlines this experience. The main screen offers two options: the first provides 10 random movie recommendations, while the second allows users to specify actor, category, or language preferences (up to 3 selections in any combination) to receive tailored recommendations. These recommendations are generated using an adjusted pagerank algorithm applied to an affiliation network.

Upon receiving recommendations, users can click on a movie title to open a new page featuring a chatbot. Initially, the chatbot provides general information about the selected movie. Users can continue interacting with the chatbot to ask additional questions about the movie.

This project's flexibility extends beyond movie recommendations; it can be adapted to offer recommendations in any domain where affiliation network data is available.

## Technologies
Project is created with **Python**. The main packages used:

* Langchain (LLM)
* Networkx (Network Analysis)
* Numpy (Data analysis and cleaning)
* Crewai (Crawling Internet for Chatbot)
* Networkx (Network analysis)
* Streamlit (Web application)

## Visualizations from project

### Visualization of the Webapp

#### Main Screen

<img width="1440" alt="Ekran Resmi 2024-04-23 20 05 24" src="https://github.com/ahbis99/movie_recommendation_system/assets/76615322/9e72bfde-6a5f-4920-b37f-9b683c5b86b5">

#### Tailored Recommendations
<img width="1440" alt="Ekran Resmi 2024-04-23 20 05 48" src="https://github.com/ahbis99/movie_recommendation_system/assets/76615322/34495c92-152c-46b5-8395-d5c4831b3d7c">
<img width="1440" alt="Ekran Resmi 2024-04-23 20 06 10" src="https://github.com/ahbis99/movie_recommendation_system/assets/76615322/551d3c6a-23d7-443d-aca2-22e32e9fffc8">
<img width="1440" alt="Ekran Resmi 2024-04-23 20 06 26" src="https://github.com/ahbis99/movie_recommendation_system/assets/76615322/7b6a3a6b-805b-4517-875a-42be7586b0da">

#### Chatbot
<img width="1440" alt="Ekran Resmi 2024-04-23 20 08 54" src="https://github.com/ahbis99/movie_recommendation_system/assets/76615322/30c576f9-a8a5-40ae-9d5a-8a5820a146ea">
<img width="1440" alt="Ekran Resmi 2024-04-23 20 09 42" src="https://github.com/ahbis99/movie_recommendation_system/assets/76615322/53ff70d3-c2f8-45ba-b3ef-fdc4c04f53af">




