function populateprimaryselect(){
    // Populate primary select dropdown
    $.ajax({
        type: 'POST',
        url: '/populateprimaryselect'
        }).done(function(data){
            $("#primaryselect").empty().append(new Option("---", 0));
            if(data){
                $.each(data, function(index, category){
                    $("#primaryselect").append(new Option(category.category_name, category.category_id));
                });
            }
    });
}

$(document).ready(function() {


    $("#addcategorybutton").on('click', function() {
        $("#remove-category-div").hide();
        $("#add-category-div").show();
    });

    $("#deletecategorybutton").on('click', function() {
        $("#add-category-div").hide();
        $("#remove-category-div").show();
    });

    // Populate primary select dropdown
    populateprimaryselect();

    $("#primaryselect").on('change', function(){
        let optionId = $("select[name=primaryselect] option").filter(':selected').val();
        if(optionId == 0){
            $("#secondary-select-dropdown").hide();
            $("#secondarybool").prop('checked', false);
        }
        else{
            $.ajax({
                data:{
                    'category_id': optionId
                },
                type: 'POST',
                url: '/populatefilteredselect'
            })
            .done(function(data){
                $("#secondary-select-dropdown").hide();
                $("#secondarybool").prop('checked', false);
                $("#secondaryselect").empty().append(new Option("---", 0));
                if(data){
                    $.each(data, function(index, category){
                        $("#secondaryselect").append(new Option(category.category_name, category.category_id));
                    });
                    $("#secondary-select-dropdown").show();
                }

            });
            
        }
        
        
    });

    $("#primarybool").on('change', function(){
        if ($('#primarybool').is(':checked')) {
            $(".subcategory").hide();
        }
        else {
            $(".subcategory").show();
        }
    });
    $("#secondarybool").on('change', function(){
        if ($('#secondarybool').is(':checked')) {
            $("#secondary-select-dropdown").hide();
        }
        else {
            $("#secondary-select-dropdown").show();
        }
    });

    // not sure if this is needed or not.
    $("#add-category-form").on('submit', function(e){
        e.preventDefault();

        let okay = false;

        let category_name = $("#categoryname").val();
        let primarybool = $('#primarybool').is(':checked');
        let primary_id = $("select[name=primaryselect] option").filter(':selected').val();
        let primary_name = $("select[name=primaryselect] option").filter(':selected').html();
        let secondarybool = $('#secondarybool').is(':checked');
        let secondary_id = $("select[name=secondaryselect] option").filter(':selected').val();
        let secondary_name = $("select[name=secondaryselect] option").filter(':selected').html();
        let postjson = {
            category_name: category_name,
            primarybool: primarybool,
            secondarybool: secondarybool,
            primary_id: primary_id,
            secondary_id: secondary_id
            };

        if(primarybool){
            okay = confirm("Create " + category_name + " as a primary category?");
        }
        else if(secondarybool){
            okay = confirm("Create " + category_name + " as a subclass of " + primary_name + "?");
        }
        else if(!primarybool && !secondarybool){
            if(primary_id == 0 || primary_id == 'undefined'){
                alert("At least 1 option must be selected to create a category!");
            }
            else if(secondary_id == 'undefined' || secondary_id == 0){
                alert("Choose a subcategory or check the box to create one!");
            }
            else{
                okay = confirm("Create " + category_name + " as a subclass of " + primary_name + " and " + secondary_name + "?");
            }
        }

        
        if(okay){
            $.ajax({
                type:'POST',
                url:'/addcategorytodb',
                data: JSON.stringify(postjson),
                contentType: "application/json"
            })
            .done(function(returned){
                $("#add-category-form").each(function(){this.reset();});
                $(".subcategory").show();
                $("#secondary-select-dropdown").hide();
                populateprimaryselect();
                alert(returned);
            });
        }
    });

});