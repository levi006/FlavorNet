# FlavorNet

## Table of Contents
- [Introduction](#introduction)
- [Technologies](#technologies)
- [Data](#the-data)
- [Project Structure](#project-structure)
- [Next Steps](#project-structure) 

## Introduction

FlavorNet is an interactive reference that allows users to discover flavor pairings based on flavor compound analysis. By modeling the relationships between flavor compounds, ingredients, ingredient prevalence, recipes and regional cuisines, users are able to discover new, possibly non-intuitive flavor combinations or ingredient substitutions. Combinatorial analysis also allows users to experiment with mapping flavor profiles within the context of a given cuisine. For example, a search for ingredient pairings with "egg" in Russian cuisine would return different ingredient combinations than a search for "egg" in Vietnamese cuisine. 


## Technologies

**Backend**

Python, Flask, SQLAlchemy, SQLite, AJAX

**Frontend**

D3.js, Javascript, Jinja, Jquery, HTML, CSS, Bootstrap

## The Data

The source datasets for the project is publicly available on [YY Ahn's](http://yongyeol.com/) website. The recipe datasets with cuisine information was scraped from the recipe aggregator sites allrecipes.com, etc.(look this up in the paper)  

## Project Structure 

## Comparing Ingredients (Query 1)

Users can search for an ingredient and generate a list of foods that contain the same flavor compounds. 

Results are represesnted using a force layout visualization. 

## Comparing Ingredients within a Cuisine (Query 2)

Users can search for an ingredient in the context of a single cuisine and generate a list of most common ingredient pairs within the cuisine. 

Results are represented using a collapsible Reingold Tilford tree, where users can click through to explore ingredient combinatins. 

##Constructing Data Tables 

- difficulty in seeding the tables
- preset queries allow for direct query of a data vs. dynamic sql queries (which take a long time)
- construction relationship tables
- combinatorics methods 

##Data Visualization

[![Demo](https://github.com/levi006/FlavorNet/blob/master/static/img/runthrough.gif)


##Further Steps 