var offImage = "https://audience.withoutabox.com/images/star-off.jpg";
var onImage = "https://audience.withoutabox.com/images/star-on.jpg";

var Stars = function() { };
gStarId = 0;

Stars.createStars = function(name){
  var starContainer = document.createElement('div');
  $(name).after(starContainer);

  for(var i = 1; i <= 5; i++){
    var star = document.createElement('img');
    $(starContainer).append(star);
    star.id = gStarId;
    var starid = "#" + star.id;
    gStarId++;
    star.name = 'star_' + i;
    star.src = offImage;
    $(starid).data('ele', name);
    $(starid).data('position', i + "");
    $(starid).click(
      function(){
        $(this).attr('src', onImage);
        $(this).prevAll().attr('src', onImage);
        $(this).nextAll().attr('src', offImage);
        $($(this).data('ele')).attr('value',$(this).data('position'));
      });
  }
};