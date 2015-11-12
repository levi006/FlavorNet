# FlavorNet

## Table of Contents
- [Introduction](#introduction)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Next Steps](#project-structure) -->

## Introduction

FlavorNet is an interactive reference that allows users to discover flavor pairings based on flavor compound analysis. By modeling the relationships between flavor compounds, ingredients, ingredient prevalence, recipes and regional cuisines, users are able to discover new, possibly non-intuitive flavor combinations or ingredient substitutions. Combinatorial analysis also allows users to experiment with mapping flavor profiles within the context of a given cuisine. For example, a search for ingredient pairings with "egg" in Russian cuisine would return different ingredient combinations than a search for "egg" in Vietnamese cuisine. 


## Technologies

**Backend**

Python, Flask, SQLAlchemy, SQLite, AJAX

**Frontend**

D3.js, Javascript, Jinja, Jquery, HTML, CSS, Bootstrap

## The Data

The source datasets for the project is publicly available on [YY Ahn's](http://yongyeol.com/) website. The recipe datasets with cuisine information was scraped from the recipe aggregator sites allrecipes.com, etc.(look this up in the paper)  

## Comparing Ingredients (Query 1)

Users can search for an ingredient and generate a list of foods that contain the same flavor compounds. 

## Comparing Ingredients within a Cuisine (Query 2)

Users can search for an ingredient and generate a list of foods that contain the same flavor compounds. 

##Constructing Data Tables 

- difficulty in seeding the tables
- preset queries allow for direct query of a data vs. dynamic sql queries (which take a long time)
- construction relationship tables
- combinatorics methods 

##Data Visualization

-D3.js
-Discussing trees vs. force layout 



##Further Steps 