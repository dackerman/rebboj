var emptyStar = "/images/star-0-";
var fullStar = "/images/star-100-";

var partialStars = [
  "/images/star-0-",
  "/images/star-25-",
  "/images/star-50-",
  "/images/star-75-",
  "/images/star-100-"
];

gStarId = 0;

var Stars = function() { };

Stars.createStars = function(id, number, tiny){
  var suffix = (tiny ? "tiny.png" : "big.png");
  // Generate HTML for whole stars.
  var container = $("#"+id);
  var wholeStars = Math.floor(number);
  for(var i=0;i<wholeStars;i++){
    Stars.createStar(container, fullStar + suffix);
  }

  // If we already displayed 5 stars, then we're done.
  if(wholeStars >= 5)
    return;

  // Generate HTML for a partial star if number isn't whole.
  var partialStar = Math.round((number - wholeStars) * 4);
  var partialImage = partialStars[partialStar] + suffix;
  Stars.createStar(container, partialImage);

  // Generate Empty stars up to 5.
  for(var i=0;i<4 - wholeStars;i++){
    Stars.createStar(container, emptyStar + suffix);
  }
};

Stars.createStar = function(container, image){
  var star = document.createElement('img');
  star.src = image;
  container.append(star);
};

Stars.createInteractiveStars = function(name){
  var suffix = "big.png";
  var starContainer = document.createElement('div');
  $(name).after(starContainer);

  for(var i = 1; i <= 5; i++){
    var star = document.createElement('img');
    $(starContainer).append(star);
    star.id = "__starid" + gStarId;
    var starid = "#" + star.id;
    star.name = 'star_' + i;
    star.src = emptyStar + suffix;
    $(starid).data('ele', name);
    $(starid).data('position', i + "");
    $(starid).attr('class', 'star');
    $(starid).click(
      function(){
        $(this).attr('src', fullStar + suffix);
        $(this).prevAll().attr('src', fullStar + suffix);
        $(this).nextAll().attr('src', emptyStar + suffix);
        $($(this).data('ele')).attr('value',$(this).data('position'));
      });
    gStarId++;
  }
};