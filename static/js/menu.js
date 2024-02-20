
let burger = document.querySelector(".burger");
let menu = document.querySelector(".menu-container");

burger.addEventListener("click", function() {
    burger.classList.toggle("activebrgr");

    if(menu.classList.contains("activemenu")){
        menu.classList.remove("activemenu");
        menu.classList.add("deactivatemenu");
    }
    else {
        menu.classList.add("activemenu");
        menu.classList.remove("deactivatemenu");
    }
});