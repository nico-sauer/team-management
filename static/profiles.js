//LOAD DOM//

$(document).ready(function () {



    //GET JSON DATA USING AN AJAX HTTP GET REQUEST//

    $.getJSON(
        'http://localhost/profiles/athletes', //API URL//

       


        function athlete_list(data) {
            var AthleteHTML = '';
            $.each(data.results, function (i, athlete) {
                //BUILD HTML TO DISPLAY PHOTOS IN PAGE//
                AthleteHTML += '<li class="athlete-list">';
                
                
                
                  //BUILD HTML TO DISPLAY NAMES IN PAGE//
                AthleteHTML += '<div class="athlete-info">';
                AthleteHTML += '<span class="athlete-name">' + athlete.first_name + ' ' + athlete.last_name + '</span>' + '<br>'
                 //BUILD HTML TO DISPLAY EMAILS IN PAGE//
                AthleteHTML +=   '<span class="athlete-email">' + athlete.email + '</span>' + '<br>'
                //BUILD HTML TO DISPLAY LOCATIONS IN PAGE//
              
                //BUILD HTML TO DISPLAY BUTTONS IN PAGE//
                 
               AthleteHTML += '<button class="detailsButton">More Details </button>' 
                
             '</div>' 

               //BUILD THE MODAL
               AthleteHTML += '<div id="athleteModal" class="modal">'
                AthleteHTML += '<div class="modal-content">'
               AthleteHTML += '<span class="close">&times;</span>' +
                               '<p>'     
                            //BUILD HTML TO DISPLAY PICTURES IN PAGE//
                
                AthleteHTML +=  '<span class="athlete-name-modal"><b>Name:</b> ' + athlete.first_name + ' ' + athlete.last_name + '</span>' + '<br>'
                
                //BUILD HTML TO DISPLAY USERNAMES IN PAGE//
               
                 //BUILD HTML TO DISPLAY EMAILS IN PAGE//
                AthleteHTML += '<span class="athlete-email-modal"><b>E-mail:</b> ' + athlete.email + '<br>' + '</span>'
                
                //BUILD HTML TO DISPLAY CELLPHONES IN PAGE//
                AthleteHTML += '<span class="athlete-cellphone-modal"><b>Phone:</b> +' +
                athlete.phone_number + '<br>' + '</span>'   
                
                  //BUILD HTML TO DISPLAY DETAILED ADDRESS IN PAGE//
              
              //BUILD HTML TO DISPLAY DOB IN PAGE//
                AthleteHTML += '<span class="athlete-dob-modal"><b>Birthday:</b> ' + 
                new Date(Date.parse(athlete.birthday.date)).toLocaleDateString(navigator.location); + '<br>' +  '</span>'   
              
                AthleteHTML += "</p></div></div></div></li>";


               });


            $('#athlete_list').html(AthleteHTML);


             // Get the modal

            $(".detailsButton").click(e => $(e.target).next().css("display", "block"));   // ALL buttons
            $(".close").click(e => $(e.target).parent().parent().css("display", "none")); // ALL close spans  

                   
                    
            }); //GET JSON DATA END
            }); //LOAD DOM END