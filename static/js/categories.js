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

$(document).ready(function(){
    
    populateprimaryselect();

    $("#primaryselect").on('change', function(){
        let optionId = $("select[name=primaryselect] option").filter(':selected').val();
        populatesecondaryselect(optionId);
        populatetertiaryselect(0);
    });

    $("#secondaryselect").on('change', function(){
        let optionId = $("select[name=secondaryselect] option").filter(':selected').val();
        populatetertiaryselect(optionId);
    });

});