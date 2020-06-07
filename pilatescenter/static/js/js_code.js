$(document).ready(function(){
  $.get( "http://127.0.0.1:8000/users/UserAPI/", function(data){$('#p1').html("data");});
});
