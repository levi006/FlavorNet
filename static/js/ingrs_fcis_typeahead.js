var substringMatcher = function(strs) {
  // console.log("We're inside substringMatcher!!")
  return function findMatches(q, cb) {
    // console.log("We're inside findMatches!!")
    var matches, substringRegex;
 
    // an array that will be populated with substring matches
    matches = [];
 
    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');
 
    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(strs, function(i, str) {
      if (substrRegex.test(str)) {
        matches.push(str);
      }
    });
 
    cb(matches);
  };
};

var ingredients_list = [];

var cuisines_list = [];

$(document).ready(function(){

$.getJSON( "/ingredients.json", function( data ) {

$.each( data, function( key, val ) {
    ingredients_list.push(key);

  });
});

$('#ingredient_pairs_typeahead .typeahead').typeahead({
    hint:true,
    highlight:true,
    minLength:1
  },
  {
    name:'ingredients_list',
    source: substringMatcher(ingredients_list) 

  });

$.getJSON( "/cuisines.json", function( data ) {

$.each( data, function( key, val ) {
    cuisines_list.push(key);
// console.log(key)
  });
});

$('#cuisines_typeahead .typeahead').typeahead({
    hint:true,
    highlight:true,
    minLength:1
  },
  {
    name:'cuisines_list',
    source: substringMatcher(cuisines_list) 

  });

});




