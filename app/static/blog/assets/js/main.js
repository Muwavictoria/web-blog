// ==============================left sidebar js================================
$(document).on('click', '#sidebar li', function(){
    $(this).addClass('active').siblings().removeClass('active')
});


// ==================================left menu sid bardp toggle=================================

$(".sub-menu ul").hide();
$(".sub-menu a").click(function() {
    $(this).parent(".sub-menu").children("ul").slideToggle("100");
    $(this).find(".right").toggleClass("fa-caret-up fa-caret-down");
});




// ===============side bar Tooggle=================================
$(document).ready(function(){
    $("#toggleSidebar").click(function(){
        $(".left-menu").toggleClass("hide");
        $(".content-wrapper").toggleClass("hide");
    });
});



// searchbar box and icon 
let search = document.querySelector('.search-box');


document.querySelector('#search-icon').onclick = () =>{
    search.classList.toggle('active');
}

// search box blog
let search2 = document.querySelector('.search-box-blog');

document.querySelector('#search-icon-blog').onclick = () =>{
    search2.classList.toggle('active')
}