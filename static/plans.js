document.addEventListener('DOMContentLoaded', function() {
});

function calculateCalories() {

  setTimeout(function () {

    // get form
    var form = document.forms["tdeeform"];

    // get sex value
    var sex = form.elements["sex"];
    if(sex[0].checked) {
      sex = 5;
    }
    else {
      sex = -161;
    }
    console.log(sex);

    // Activity level array
    var activity_multiplier = new Array();
    activity_multiplier[1] = 1.2;
    activity_multiplier[2] = 1.375;
    activity_multiplier[3] = 1.55;
    activity_multiplier[4] = 1.725;
    activity_multiplier[5] = 1.9;

    // get activity level 
    activitylevel_value = 0;
    var activityselected = form.elements["activitylevel"].value;
    activitylevel_value = activity_multiplier[activityselected];
    console.log(activitylevel_value);

    // get weight
    var weight = form.elements["weight"].value;
    console.log(weight);

    // get height
    var height = form.elements["height"].value;
    console.log(height);

    // get age
    var age = form.elements["age"].value;
    console.log(age);

    // Calculate calories
    calories_result = ((weight * 10) + (height * 6.25) - (5 * age) + sex) * activitylevel_value;

    // Update view
    document.getElementById('calories_result').innerHTML = calories_result.toFixed(0);


  }, 1);

}

