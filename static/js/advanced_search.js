function populateprimaryselect(){
    // Populate primary select dropdown
    $.ajax({
        type: 'POST',
        url: 'populateprimaryselect'
        }).done(function(data){
            $("#primaryselect").empty().append(new Option("---", 0));
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
        $("#secondaryselect").empty().append(new Option("---", 0));
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
        $("#tertiaryselect").empty().append(new Option("---", 0));
        if(data){
            $.each(data, function(index, category){
                $("#tertiaryselect").append(new Option(category.category_name, category.category_id));
            });
        }
    });
}

function secondaryfiltertoggle(){
    $("#secondaryfilterbool").on('change', function(){
        if ($("#secondaryfilterbool").is(':checked')) {
            $(".secondary-wraper").show();
            $("#secondaryselect").prop('disabled', false);
            $("#tertiary-form-row").show();
        }
        else {
            $(".secondary-wraper").hide();
            $("#secondaryselect").prop('disabled', false);
            $("#tertiary-form-row").hide();
            $(".tertiary-wraper").hide();
            $("#tertiaryfilterbool").prop("checked", false);
            $("#tertiaryselect").prop('disabled', true);
        }
    });
}

function tertiaryfiltertoggle(){
    $("#tertiaryfilterbool").on('change', function(){
        if ($("#tertiaryfilterbool").is(':checked')) {
            $(".tertiary-wraper").show();
            $("#tertiaryselect").prop('disabled', false);
        }
        else {
            $(".tertiary-wraper").hide();
            $("#tertiaryselect").prop('disabled', true);
        }
    });
}


$(document).ready(function(){
    populateprimaryselect();
    secondaryfiltertoggle();
    tertiaryfiltertoggle();

    $("#primaryselect").on('change', function(){
        let primeoptionId = $("select[name=primaryselect] option").filter(':selected').val();
        populatesecondaryselect(primeoptionId);
        $("#secondary-form-row").show();
        $("#tertiary-form-row").hide();
        $(".tertiary-wraper").hide();
        $("#tertiaryfilterbool").prop("checked", false);
    });

    $("#secondaryselect").on('change', function(){
        let secondaryoptionId = $("select[name=secondaryselect] option").filter(':selected').val();
        populatetertiaryselect(secondaryoptionId);
        $("#tertiary-form-row").show();
    });

});

// Add filters to list
// TODO: add check to prevent multiple additions
function add_to_filters(selected){
    var sub_cat = selected.options[selected.selectedIndex];
    var filter_list = document.getElementById("filter-list");
    var filter_elements = filter_list.getElementsByTagName("li");
    // Create clear all button if empty
    if(filter_elements.length === 0){
        var clearall = document.createElement("li");
        clearall.value = 0;
        clearall.className = "filter-tag-clear-all"
        clearall.onclick = clear_all_filters;
        var clearbutton = document.createElement("button");
        clearbutton.type = "button";
        clearbutton.value = "clear-all"
        clearbutton.className = "filter-tag clear-all";
        clearbutton.innerHTML = "Clear All";
        clearall.appendChild(clearbutton);
        filter_list.append(clearall);
    }    
    // call function to check if value is in list already
    if(!contains_filter(filter_elements, sub_cat.value)){
        let filter = document.createElement("li");
        filter.className = "filter-tag";
        filter.value = sub_cat.value;
        let filter_button = document.createElement("button");
        filter_button.className = "filter-tag-button";
        filter_button.type = "button";
        filter_button.value = sub_cat.value;
        filter_button.onclick = remove_from_filters();
        filter_button.innerHTML = sub_cat.text + " <i class='fas fa-times'></i>";
        filter.appendChild(filter_button);
        let filter_input = document.createElement("input");
        filter_input.type = "hidden";
        filter_input.value = sub_cat.value;
        filter_input.name = "filterID";
        filter.appendChild(filter_input);
        filter_list.prepend(filter);
    }
}
// check if ul contains value
function contains_filter(list, liValue){
    for(let index = 0; index < list.length; index++){
        if(Number(list[index].value) == liValue){
            return true;
        }
    }
    return false;
}

// Remove filters from list
// TODO: implement later
function remove_from_filters(){

}
// Remove all filters from list
function clear_all_filters(){
    let filter_list = document.getElementById("filter-list");
    while(filter_list.firstChild){
        filter_list.removeChild(filter_list.firstChild);
    }
}