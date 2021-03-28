// Populates selector options
function init(){
    populate_primary();
    console.table(global_categories);
    console.table(global_sub);
}
// Populate options in primary selector
function populate_primary(){
    var catetory_selector = document.getElementById("category-selector");
    catetory_selector.options.length = 0; // clear any data in selector
    let category_option = document.createElement("option");
    // Create blank option
    category_option.value = "0";
    category_option.text = "Show All";
    category_option.selected = true;
    catetory_selector.add(category_option);
    // Loop to populate from json
    for (var i = 0; i < global_categories.length; i++){
        category_option = document.createElement("option");
        category_option.value = global_categories[i]['cat_id'];
        category_option.text = global_categories[i]['name'];
        catetory_selector.add(category_option);
    }
    // Populates the subcategories with all elements
    populate_sub(0);
}
// Populate subcategory
function populate_sub(category_id){
    var sub_selector = document.getElementById("subcategory-selector");
    sub_selector.options.length = 0; // clear any data in selector
    // if id = star, show all
    if(category_id === 0){
        // Loop to populate from json
        for (var i = 0; i < global_sub.length; i++){
            let category_option = document.createElement("option");
            category_option.value = global_sub[i]['sub_id'];
            category_option.text = global_sub[i]['sub_name'];
            sub_selector.add(category_option);
        }
    }
    // else show by the filtered id
    else{
        for (i = 0; i < global_sub.length; i++){
            // Check if selected category matches the parent category
            if(category_id === Number(global_sub[i]['parent_category'])){
                let category_option = document.createElement("option");
                category_option.value = global_sub[i]['sub_id'];
                category_option.text = global_sub[i]['sub_name'];
                sub_selector.add(category_option);
            }
        }
    }
}
// Filters the subcategory
function filter_sub(selected){
    let category_value = Number(selected.options[selected.selectedIndex].value);
    populate_sub(category_value);
}
