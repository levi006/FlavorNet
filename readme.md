# FlavorNet

## Table of Contents
- [Introduction](#introduction)
- [Technologies](#technologies)
- [The Data](#the-data)
- [Project Structure](#project-structure)
 

## Introduction

FlavorNet is an interactive reference that allows users (molecular gastronomy geeks) to discover flavor pairings based on flavor compound analysis. By modeling the relationships between flavor compounds, ingredients, ingredient prevalence, recipes and regional cuisines, users are able to discover new, possibly non-intuitive flavor combinations or ingredient substitutions. Combinatorial analysis also allows users to experiment with mapping flavor profiles within the context of a given cuisine. For example, a search for ingredient pairings with "egg" in Russian cuisine would return different ingredient combinations than a search for "egg" in Vietnamese cuisine. 

![Demo](https://github.com/levi006/FlavorNet/blob/master/static/img/runthrough.gif)

## Technologies

**Backend**

Python, Flask, SQLAlchemy, SQLite, AJAX

**Frontend**

D3.js, Javascript, Jinja, Jquery, HTML, CSS, Bootstrap

## The Data

The source data sets for the project are publicly available on [YY Ahn's](http://yongyeol.com/) website. The recipe data sets were scraped from the recipe aggregator sites allrecipes.com, epicurious.com and menupan.com. 

## Project Structure 

#### Query 1: Comparing Ingredients

This logic behind this query is simply the number of flavor compounds a given ingredient has in common with a second ingredient. 

#### Query 2: Comparing Ingredients within a Cuisine

Initially I flirted with using k-means to classify ingredients based on common flavor commpounds, but given the relative sparsity of the data set, I decided in favor of creating a relational table that tracked ingredient pairs within a given cuisine and the number of times the respective ingredient pair and cuisine appeared in the data set.     

The itertools library was instrumental to track all possible discrete ingredient pair-cuisine combinations and discard duplicate permutations (i.e. "broccoli and kale in Italian cuisine" is the same as "kale and broccoli in Italian cuisine" and not two different combinations). 
