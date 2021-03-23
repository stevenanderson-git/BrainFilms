

function ddlselect(selected){
    console.log(selected.options[selected.selectedIndex])
    let category_value = selected.options[selected.selectedIndex].value;
    let category_name = selected.options[selected.selectedIndex].text;
    document.getElementById("current-selected-category").innerHTML = category_value;
    let sub_selector = document.getElementById("subcategory-selector");
    // clear any previous options
    sub_selector.options.length = 0;
    let sub_option = document.createElement("option");
    sub_option.value = category_value;
    sub_option.name = category_name;
    sub_option.text = category_name;
    sub_selector.add(sub_option);
}
function pop_subs(parent_category){
    let categoryselector = document.getElementById("category-selector");
    let option = document.createElement("option");
    option.text = "test";
    categoryselector.add(option);
}

// this should add to a list and the list items could be removed/added
function update_display(subcategory){
    let sub_value = subcategory.options[subcategory.selectedIndex].value;
    let sub_name = subcategory.options[subcategory.selectedIndex].text;
    document.getElementById("current-selected-category").innerHTML = sub_value + " " + sub_name;
}
