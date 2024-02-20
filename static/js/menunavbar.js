let profile = document.getElementById("menu-navbar");

profile.addEventListener("click", function() {
    var profile_menu = document.getElementById("profileMenu");
    if(profile_menu.classList.contains("activeprofile-menu")){
        profile_menu.classList.remove("activeprofile-menu");
        profile_menu.classList.add("deactiveprofile-menu");
    }
    else {
        profile_menu.classList.add("activeprofile-menu");
        profile_menu.classList.remove("deactiveprofile-menu");
    }

});   