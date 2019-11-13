
// Get the modal
var addRecipeModal = document.getElementById("myModal");
var addTagModal = document.getElementById("addTagModal");
var advancedSearchModal = document.getElementById("advancedSearchModal")

// Get the button that opens the modal
var btn = document.getElementById("myBtn");
var addTagButton = document.getElementById("addTagButton");
var advancedSearchButton = document.getElementById("advancedSearchButton");

// Get the <span> element that closes the modal
var addRecipeClose = document.getElementById("addRecipeClose");
var addTagClose = document.getElementById("addTagClose");

if (addRecipeModal !== null){
    // When the user clicks the button, open the modal 
    btn.onclick = function() {
        addRecipeModal.style.display = "block";
    }
        
    // When the user clicks on <span> (x), close the modal
    addRecipeClose.onclick = function() {
        addRecipeModal.style.display = "none"
    }
}

if (addTagModal !== null){
    // When the user clicks the button, open the modal 
    addTagButton.onclick = function() {
        addTagModal.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modal
    addTagClose.onclick = function() {
        addTagModal.style.display = "none"
    }
}


if (advancedSearchModal !== null){
    // When the user clicks the button, open the modal 
    advancedSearchButton.onclick = function() {
        advancedSearchModal.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modal
    advancedSearchClose.onclick = function() {
        advancedSearchModal.style.display = "none"
    }
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == addRecipeModal) {
        addRecipeModal.style.display = "none";
    } 
    if (event.target == addTagModal) {
        addTagModal.style.display = "none";
    }
    if (event.target == advancedSearchModal) {
        advancedSearchModal.style.display = "none";
    }
}
