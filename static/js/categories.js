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
        let selected = $("select[name=primary] option").filter(':selected').val();
        if( selected == 8){
            $(".secondary").show();
        }
        else{
            $(".secondary").hide();
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
    $("#add-category-form").on('submit', function(e){
        e.preventDefault();
        $.ajax({
            type:'POST',
            url:'/admin/dashboard',
            data:{
              todo:$("#categoryname").val()
            },
            success:function()
            {
              alert('saved');
            }
          })
    });

});