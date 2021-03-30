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
// Add filters to list
// TODO: add check to prevent multiple additions
function add_to_filters(selected){
    let sub_cat = selected.options[selected.selectedIndex];
    let filter_list = document.getElementById("filter-list");
    // Create clear all button if empty
    if(filter_list.innerHTML===""){
        let clearall = document.createElement("li");
        let clearbutton = document.createElement("button");
        clearbutton.type = "button";
        clearbutton.value = "clear-all"
        clearbutton.className = "filter-tag clear-all";
        clearbutton.onclick = clear_all_filters();
        clearbutton.innerHTML = "Clear All";
        clearall.appendChild(clearbutton);
        filter_list.append(clearall);
    }

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
    filter_list.prepend(filter);
}
// Remove filters from list
function remove_from_filters(){

}
// Remove all filters from list
function clear_all_filters(){
    let filter_list = document.getElementById("filter-list");
    filter_list.length = 0;
}