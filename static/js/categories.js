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

    $("#parentbool").on('change', function(){
        if ($('#parentbool').is(':checked')) {
            $(".subcategory").hide();
        }
        else {
            $(".subcategory").show();
        }
    });

    // not sure if this is needed or not.
    $("#add-category-form").on('submit', function(e){
        e.preventDefault();
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
          })
    });

});