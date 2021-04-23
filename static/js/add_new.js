function populateprimaryselect(){
    // Populate primary select dropdown
    $.ajax({
        type: 'POST',
        url: 'populateprimaryselect'
        }).done(function(data){
            $("#primaryselect").empty().append(new Option("None", 0));
            if(data){
                $.each(data, function(index, category){
                    $("#primaryselect").append(new Option(category.category_name, category.category_id));
                });
            }
    });
}

function populatesecondaryselect(optionId){
    $.ajax({
        data:{
            'category_id': optionId
        },
        type: 'POST',
        url: '/populatefilteredselect'
    })
    .done(function(data){
        $("#secondaryselect").empty().append(new Option("None", 0));
        if(data){
            $.each(data, function(index, category){
                $("#secondaryselect").append(new Option(category.category_name, category.category_id));
            });
        }
    });
}

function populatetertiaryselect(optionId){
    $.ajax({
        data:{
            'category_id': optionId
        },
        type: 'POST',
        url: '/populatefilteredselect'
    })
    .done(function(data){
        $("#tertiaryselect").empty().append(new Option("None", 0));
        if(data){
            $.each(data, function(index, category){
                $("#tertiaryselect").append(new Option(category.category_name, category.category_id));
            });
        }
    });
}

function subbooltoggle(){
    $("#showsubbool").on('change', function(){
        if ($("#showsubbool").is(':checked')) {
            $("#subcategorydiv").show();
        }
        else {
            $("#subcategorydiv").hide();
        }
    });
}

function filterfurtherbooltoggle(){
    $("#filterfurtherbool").on('change', function(){
        if ($('#filterfurtherbool').is(':checked')) {
            $("#tertiary-selector-div").show();
        }
        else {
            $("#tertiary-selector-div").hide();
        }
    });
}

function resetonprimary(){
    $("#showsubbool").prop("checked", false);
    $("#subcategorydiv").hide();
    
    $("#filterfurtherbool").prop("checked", false);
    $("#tertiary-selector-div").hide();
    
}

function resetonsecondary(){
    $("#filterfurtherbool").prop("checked", false);
    $("#tertiary-selector-div").hide();
}


$(document).ready(function(){

    subbooltoggle();
    filterfurtherbooltoggle();    
    populateprimaryselect();

    $("#primaryselect").on('change', function(){
        let primeoptionId = $("select[name=primaryselect] option").filter(':selected').val();
        if(primeoptionId == 0){
            resetonprimary();
            $("#choosesubdiv").hide();
        }
        else{
            populatesecondaryselect(primeoptionId);
            resetonprimary();
            $("#choosesubdiv").show();
        }
    });

    $("#secondaryselect").on('change', function(){
        let secondaryoptionId = $("select[name=secondaryselect] option").filter(':selected').val();
        if(secondaryoptionId == 0){
            resetonprimary();
        }
        else{
            populatetertiaryselect(secondaryoptionId);
            resetonsecondary();
            $("#filterfurtherdiv").show();
        }
    });

    $("#tertiaryselect").on("change", function(){
        let tertiaryoptionId = $("select[name=tertiaryselect] option").filter(':selected').val();
        if(tertiaryoptionId == 0){
            resetonsecondary();
        }
    });

    $("#addvideoform").on("submit", function(e){
        e.preventDefault();
        let okay = false;
        
        let video_title = $("#video_title").val();
        let video_url = $("#video_url").val();
        let primeoptionId = $("select[name=primaryselect] option").filter(':selected').val();
        let primeoptionname = $("select[name=primaryselect] option").filter(':selected').html();
        let secondaryoptionId = $("select[name=secondaryselect] option").filter(':selected').val();
        let secondaryoptionname = $("select[name=secondaryselect] option").filter(':selected').html();
        let tertiaryoptionId = $("select[name=tertiaryselect] option").filter(':selected').val();
        let tertiaryoptionname = $("select[name=tertiaryselect] option").filter(':selected').html();
        let secondarybool = $("#showsubbool").is(':checked');
        let tertiarybool = $('#filterfurtherbool').is(':checked');      
        let category_id = 0;

        if(tertiarybool){
            if(typeof tertiaryoptionId === "undefined" || tertiaryoptionId == 0){
                alert("A category must be selected that is not None.")
            }
            else{
                category_id = tertiaryoptionId;
                okay = confirm("Add " + video_title + " under category " + tertiaryoptionname + "?");
            }
        }
        else if(secondarybool && !tertiarybool){
            if(typeof secondaryoptionId === "undefined" || secondaryoptionId == 0){
                alert("A category must be selected that is not None.")
            }
            else{
                category_id = secondaryoptionId;
                okay = confirm("Add " + video_title + " under category " + secondaryoptionname + "?");
            }
        }
        else if(!secondarybool && !tertiarybool){
            if(typeof primeoptionId === "undefined" || primeoptionId == 0){
                alert("A category must be selected that is not None.")
            }
            else{
                category_id = primeoptionId;
                okay = confirm("Add " + video_title + " under category " + primeoptionname + "?");
            }
        }

        let newVideoJson = {
            video_title: video_title,
            video_url: video_url,
            category_id: category_id
        }

        if(okay){
            console.log(newVideoJson);
            $.ajax({
                type: 'POST',
                url: '/addvideotodb',
                data: JSON.stringify(newVideoJson),
                contentType: 'application/json'
            })
            .done(function(returned){
                alert(returned);
            });
        }




    });
});