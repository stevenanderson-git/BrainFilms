$(document).ready(function() {
    $("#submit-button").on('click', function() {
        console.log('hi');
    });
    $("#category").on('change', function(){
        let selected = $("select[name=category] option").filter(':selected').val();
        console.log(selected);
        if( selected == 8){
            $(".c2").show();
        }
        else{
            $(".c2").hide();
        }
        
    });
});