$(document).ready(function() {
    $("#addcategorybutton").on('click', function() {
        $("#remove-category-div").hide();
        $("#add-category-div").show();
    });

    $("#deletecategorybutton").on('click', function() {
        $("#add-category-div").hide();
        $("#delete-category-div").show();
    });

    $("#primary").on('change', function(){
        let optionId = $("select[name=primary] option").filter(':selected').val();
        let optionText = $("select[name=primary] option").filter(':selected').html();
        if(optionId == 0){
            $(".secondary").hide();
        }
        else{
            $.ajax({
                data:{
                    'category_id': optionId,
                    'category_name': optionText
                },
                type: 'POST',
                url: '/popsubcategory'
            })
            .done(function(data){
                $("#secondary").empty().append(new Option("---", 0))
                $.each(data, function(index, category){
                    $("#secondary").append(new Option(category.category_name, category.category_id));
                });
                $(".secondary").show();
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
        let primary_id = $("select[name=primary] option").filter(':selected').val();
        let primary_name = $("select[name=primary] option").filter(':selected').html();
        let secondarybool = $('#secondarybool').is(':checked');
        let secondary_id = $("select[name=secondary] option").filter(':selected').val();
        let secondary_name = $("select[name=secondary] option").filter(':selected').html();

        if(primarybool){
            okay = confirm("Create " + category_name + " as a primary category?");
        }
        else if(secondarybool){
            okay = confirm("Create " + category_name + " as a subclass of " + primary_name + "?");
        }
        else if(!primarybool && !secondarybool){
            if(primary_id == 0 || primary_id == 'undefined' || secondary_id == 'undefined' || secondary_id == 0){
                alert("At least 1 option must be selected to create a category!");
            }
            else{
                okay = confirm("Create " + category_name + " as a subclass of " + primary_name + " and " + secondary_name + "?");
            }
        }

        if(okay){
            $.ajax({
                type:'POST',
                url:'/admin/dashboard',
                data:{
                    categoryname:$("#categoryname").val(),
                    isparent:$("#parentbool").val(),
                    primeparent:$("#primary").val(),
                    secparent:$("#secondary").val()
                },
                dataType:'json',
                success:function(){
                    alert(data);
                }
              });
        }
    });

});