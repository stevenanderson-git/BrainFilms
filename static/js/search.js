function ddlselect(){
    let categoryselector=document.getElementById("category-selector");
    let displaytext = categoryselector.options[categoryselector.selectedIndex].value
    document.getElementById("current-selected-category").innerHTML = displaytext;
}
function popCategory(categories){
    let categoryselector = document.getElementById("category-selector");
    let option = document.createElement("option");
    option.text = "test";
    categoryselector.add(option);
}
